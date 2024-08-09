import scapy.all as scapy
import numpy as np

# https://scapy.readthedocs.io/en/latest/usage.html
# 3° pezzo di codice, implementa la tecnica di backlog scan

def backlog_syn_scan(bcklg_size, zombie_ip, zombie_port, target_subnet): # subnet must be in format "192.168.1"
    packets_number = int(bcklg_size*3/4) # we want to fill only 3/4 of the whole backlog in order not to DoS the zombie
    syn_packets_number = int(packets_number/2) # we send half of the total size of packets as SYN packets
    canaries_number = packets_number - syn_packets_number # the other half is filled with canaries
    ports = np.random.default_rng().choice([x for x in range(1024, 49151)], syn_packets_number, replace=False) # we use random ports since we don't care if they're open 
    res = []

    for i in range(256): 
        target_ip = target_subnet + '.' + i
        syn_packets = scapy.IP(dst=zombie_ip, src=target_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:packets_number], flags="S")
        canaries = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:canaries_number], flags="S", seq=1) #we care about the sequence number because the probes need to have seq-=1
        probes = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:canaries_number], flags="S", seq=0) # used to "ping" the canaries

        packets = np.random.choice(np.concatenate([syn_packets, canaries]), packets_number, replace=False)  # randomly mixing SYN packets with canaries
        scapy.send(packets, inter=1./5) # sending SYN packets mixed with canaries
        answered, unanswered = scapy.sr(probes, inter=1./5, timeout=1) # "pinging" the canaries, is the timeout ok?
        
        ack = 0.; # we need to check if target is alive  
        for packet, response in answered: 
            if response.flags == 0x10: # ACK = 0x10,  how many do we need?
                ack += 1. 
                print(response.sport, response.flags)
        print(f"Ack received: {ack}, Total canaries: {canaries_number}") # maybe if ack > treshold we consider it alive
        res.append((target_ip, ack/canaries_number))
    return res