import scapy.all as scapy
import numpy as np
from scipy.stats import hypergeom
from time import sleep
import random

# https://scapy.readthedocs.io/en/latest/usage.html

def find_p_value(trials, canaries_number, bcklg_size):
    loss1, loss2, loss3 = trials[0]['loss'], trials[1]['loss'], trials[2]['loss']
    ack1, ack2, ack3 = trials[0]['ack'], trials[1]['ack'], trials[2]['ack']
    k1, k2, k3 = trials[0]['k'], trials[1]['k'], trials[2]['k']
    
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

    K = canaries_number - loss # - (packets_number/5)
    N = 2*K
    n = N - (bcklg_size/2) # - (packets_number/5)
    p_value = hypergeom.sf(k, N, K, n) # or cdf?

    return p_value


def backlog_syn_scan(bcklg_size, zombie_ip, zombie_port, target_ip): # subnet must be in format "192.168.1"
    trials = []

    packets_number = int(bcklg_size*3/4) # we want to fill only 3/4 of the whole backlog in order not to DoS the zombie
    syn_packets_number = int(packets_number/2) # we send half of the total size of packets as SYN packets
    canaries_number = packets_number - syn_packets_number # the other half is filled with canaries
    ports = np.random.default_rng().choice([x for x in range(1024, 49151)], syn_packets_number, replace=False) # we use random ports, doesn't matter if they're open 
    
    packets = []
    
    
    
    for port in ports:
        packet = scapy.IP(dst=zombie_ip, src=target_ip)/scapy.TCP(dport=zombie_port, sport=port, flags="S")
        packets.append(packet)
        
    for port in ports:
        packet = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=port, flags="S", seq=1)
        packets.append(packet)
        
    
    probes = []
    for port in ports:
        packet = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=port, flags="S", seq=0)
        probes.append(packet)


    # for _ in range(3):
    answered, _ = scapy.sr(packets, inter=1/5, timeout=1) # sending SYN packets mixed with canaries #TODO put inter=1/5
    loss = canaries_number - len(answered)
    
    answered, _ = scapy.sr(probes, timeout=1) # "pinging" the canaries, is the timeout ok? #TODO put inter=1/5
    
    ack = 0
    sa = 0
    for _, response in answered:
        if response is not None:
            tcp_header = response.getlayer(scapy.TCP) if response.haslayer(scapy.TCP) else None
            if tcp_header is not None and tcp_header.flags == 0x10:
                ack += 1
            elif tcp_header.flags == 0x12:
                sa += 1
                
    print(f"ACKs received: {ack}, Total canaries: {canaries_number}, SA = {sa}\n") 
                
    # trials.append({'loss': loss, 'ack': ack, 'k': canaries_number - ack})
    # sleep(packets_number/5) # wait for the backlog to be processed or cleaned
    
    # p_value = find_p_value(trials, canaries_number, bcklg_size)
    return 0