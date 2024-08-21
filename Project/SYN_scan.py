import scapy.all as scapy
import numpy as np
from scipy.stats import hypergeom

# https://scapy.readthedocs.io/en/latest/usage.html
# 3° pezzo di codice, implementa la tecnica di backlog scan

def backlog_syn_scan(bcklg_size, zombie_ip, zombie_port, target_subnet): # subnet must be in format "192.168.1"
    packets_number = int(bcklg_size*3/4) # we want to fill only 3/4 of the whole backlog in order not to DoS the zombie
    syn_packets_number = int(packets_number/2) # we send half of the total size of packets as SYN packets
    canaries_number = packets_number - syn_packets_number # the other half is filled with canaries
    ports = np.random.default_rng().choice([x for x in range(1024, 49151)], syn_packets_number, replace=False) # we use random ports since we don't care if they're open 
    res = []

    for i in range(256): #TODO: update based on the network
        trials = []
        target_ip = target_subnet + '.' + i
        syn_packets = scapy.IP(dst=zombie_ip, src=target_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:packets_number], flags="S")
        canaries = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:canaries_number], flags="S", seq=1) #we care about the sequence number because the probes need to have seq-=1
        probes = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:canaries_number], flags="S", seq=0) # used to "ping" the canaries
        packets = np.random.choice(np.concatenate([syn_packets, canaries]), packets_number, replace=False)  # randomly mixing SYN packets with canaries

        for _ in range(3):
            scapy.send(packets, inter=1./5) # sending SYN packets mixed with canaries
            answered, unanswered = scapy.sr(probes, inter=1./5, timeout=1) # "pinging" the canaries, is the timeout ok?
            loss = len(unanswered)
            
            ack = 0 # we need to check if target is alive  
            for packet, response in answered: 
                if response.flags == 0x10: # ACK = 0x10
                    ack += 1. 
            print(f"ACKs received: {ack}, Total canaries: {canaries_number}\n") 
                        
            trials.append({'loss': loss, 'ack': ack, 'k': canaries_number - ack})
        
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
                if k1 == max(k1, k2, k3):
                    loss, ack, k = loss1, ack1, k1
                elif k2 == max(k1, k2, k3):
                    loss, ack, k = loss2, ack2, k2
                else:
                    loss, ack, k = loss3, ack3, k3

        K = canaries_number - loss - (packets_number/5)
        N = 2*K
        n = N - (bcklg_size/2) - (packets_number/5)
        p_value = hypergeom.cdf(k, N, K, n) # or sf?

        res.append((target_ip, p_value))
    return res