import scapy.all as scapy
import numpy
import random
import time

def search_zombie():
    pass 

def generate_random_ip():
    res = ""
    #TODO generate a random IP based on a known subnet mask
    for _ in range(4):
        res += f'{random.randint(0,255)}.'
    return res[:len(res)-1]

def search_zombies_illegal(limit=1, local_ip = "127.0.0.1", local_port = 49152):
    # ports = [21, 22, 80, 443, 632]
    ports = [4242]
    possible_candidate = []
    
    """
    TCP Flag Values:
        SYN Flag: 0x02
        ACK Flag: 0x10
        SYN-ACK Flag: Combination of SYN and ACK, which is 0x02 | 0x10 = 0x12
    """
    
    for _ in range(limit):
        # ip = generate_random_ip()
        ip = "tcpbin.com" 
        for port in ports:
            SYN = scapy.IP(dst=ip)/scapy.TCP(dport=port, flags='S', seq=1000)
            response = scapy.sr1(SYN, timeout=4, verbose=True)
            if response is not None:
                tcp_header = response.getlayer(scapy.TCP) if response.haslayer(scapy.TCP) else None
                if tcp_header is not None and (tcp_header.flags & (0x02 | 0x10)) == (0x02 | 0x10):
                    possible_candidate.append(ip)
                
    
    print(possible_candidate)


def main():
    search_zombies_illegal() 

if __name__ == "__main__":
    main()