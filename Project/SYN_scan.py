import scapy.all as scapy
import numpy as np
from scipy.stats import hypergeom
from time import sleep
import random
import logging

def find_p_value(trials, canaries_number, bcklg_size):
    """
    Find the p-value of the target machine to be alive based on the results of the trials.

    :param trials: list of dictionaries containing the results of the trials
    :param canaries_number: number of canaries sent
    :param bcklg_size: backlog size of the zombie
    :return: p_value, represent the probability of the target machine to be alive
    """
    loss1, loss2, loss3 = trials[0]['loss'], trials[1]['loss'], trials[2]['loss']
    ack1, ack2, ack3 = trials[0]['ack'], trials[1]['ack'], trials[2]['ack']
    k1, k2, k3 = trials[0]['k'], trials[1]['k'], trials[2]['k']
    
    # We choose the trial with the minimum loss, if there are no losses we choose the one with the maximum number of evictions k
    if loss1 != 0 and loss2 != 0 and loss3 != 0: 
        if loss1 == min(loss1, loss2, loss3):
            loss, ack, k = loss1, ack1, k1
        elif loss2 == min(loss1, loss2, loss3):
            loss, ack, k = loss2, ack2, k2
        else:
            loss, ack, k = loss3, ack3, k3
    else:
        zero_losses = [loss1, loss2, loss3].count(0)
        if zero_losses == 1:
            if loss1 == 0:
                loss, ack, k = loss1, ack1, k1
            elif loss2 == 0:
                loss, ack, k = loss2, ack2, k2
            else:
                loss, ack, k = loss3, ack3, k3
        else:
            if k1 == max(k1, k2, k3) and loss1 == 0:
                loss, ack, k = loss1, ack1, k1
            elif k2 == max(k1, k2, k3) and loss2 == 0:
                loss, ack, k = loss2, ack2, k2
            else:
                loss, ack, k = loss3, ack3, k3

    K = canaries_number - loss # number of successes in the population
    N = 2*K # population size, assuming that canaries_loss == spoofed_loss
    n = N - (bcklg_size/2) # number of draws taken without replacement
    p_value = hypergeom.sf(k, N, K, n) 

    logging.info(f"Loss: {loss}, ACKs: {ack}, Evicted Canaries: {k}, N: {N}, K: {K}, n: {n}, p-value: {p_value}")
    return p_value

def backlog_syn_scan(bcklg_size, zombie_ip, zombie_port, target_ip):
    """
    Check whether the target machine is alive and reachable.
    
    :param bcklg_size: zombie's backlog size
    :param zombie_ip: zombie's IP address
    :param zombie_port: zombie's port number
    :param target_ip: target's IP address
    :return: p_value, represent the probability of the target machine to be alive 
    """
    trials = []
    packets = []

    packets_number = int(bcklg_size*3/4) # we want to fill only 3/4 of the whole backlog in order not to DoS the zombie
    syn_packets_number = int(packets_number/2) # we send half of the total size of packets as SYN packets
    canaries_number = packets_number - syn_packets_number # the other half is filled with canaries
    ports = np.random.default_rng().choice([x for x in range(49151, 65535)], syn_packets_number, replace=False) # we use random ports, doesn't matter if they're open 
    
    # Creates the spoofed SYN packets
    for port in ports:
        packet = scapy.IP(dst=zombie_ip, src=target_ip)/scapy.TCP(dport=zombie_port, sport=port, flags="S")
        packets.append(packet)
    
    # Creates the canaries
    for port in ports:
        packet = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=port, flags="S", seq=1)
        packets.append(packet)

    packets = random.sample(packets, len(packets)) # shuffle randomly the packets
            
    # Creates the probes
    probes = []
    for port in ports:
        packet = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=port, flags="S", seq=0) # probes are equal to canaries with seq-=1
        probes.append(packet)

    for _ in range(3): # we repeat the process 3 times to get a more accurate result
        answered, _ = scapy.sr(packets, inter=1/5, timeout=0) # sending SYN packets mixed with canaries 
        loss = canaries_number - len(answered)
        
        answered, _ = scapy.sr(probes, timeout=5) # "pinging" the canaries by sending the probes
        
        ack = 0
        sa = 0
        for _, response in answered: # counting the number of ACKs and SYN-ACKs on the answers to the probes
            if response is not None:
                tcp_header = response.getlayer(scapy.TCP) if response.haslayer(scapy.TCP) else None
                if tcp_header is not None and tcp_header.flags == 0x10: # ACK received
                    ack += 1
                elif tcp_header.flags == 0x12: # SYN-ACK received
                    sa += 1
                    
        logging.info(f"Total canaries: {canaries_number}, ACKs: {ack},  SYN-ACKs: {sa}") 
                    
        trials.append({'loss': loss, 'ack': ack, 'k': canaries_number - ack})
        sleep(packets_number/5) # wait for the backlog to be processed or cleaned
        
    return find_p_value(trials, canaries_number, bcklg_size) # we use statistical analysis to determine the p-value