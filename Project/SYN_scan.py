import scapy.all as scapy
import numpy as np

# https://scapy.readthedocs.io/en/latest/usage.html
# 3° pezzo di codice, implementa la tecnica di backlog scan

def backlog_syn_scan(bcklg_size, zombie_ip, zombie_port, target_ip): # for now it doesn't cycle on the whole subnet
    ports = [21, 22, 80, 135, 139, 443, 445, 631] # we start from a list of common ports
    packets_number = int(bcklg_size*3/4) # we want to fill only 3/4 of the whole backlog in order not to DoS the zombie
    syn_packets_number = int(packets_number/2) # we send half of the total size of packets as SYN packets
    canaries_number = packets_number - syn_packets_number # the other half is filled with canaries
    found = False; # we need to check if target is alive

    while len(ports) < max(packets_number, canaries_number): # adding random source ports if it's needed
        random_port = np.random.randint(1024, 65535)
        if random_port not in ports:
            ports.append(random_port)

    syn_packets = scapy.IP(dst=zombie_ip, src=target_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:packets_number], flags="S")
    canaries = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:canaries_number], flags="S", seq=1) #we care about the sequence number because the probes need to have seq-=1
    probes = scapy.IP(dst=zombie_ip)/scapy.TCP(dport=zombie_port, sport=ports[0:canaries_number], flags="S", seq=0) # used to "ping" the canaries

    packets = np.random.choice(np.concatenate([syn_packets, canaries]), packets_number, replace=False)  # randomly mixing SYN packets with canaries
    scapy.send(packets, inter=1./5) # sending SYN packets mixed with canaries
    answered, unanswered = scapy.sr(probes, inter=1./5) # "pinging" the canaries
    
    for packet, response in answered: # basta che ce ne sia uno? E come tempi, devo aspettare qualcosa o posso guardare le risposte subito?
        if response.flags == "A": 
            found = True
            print(response.sport, response.flags)
            break
    
    return found