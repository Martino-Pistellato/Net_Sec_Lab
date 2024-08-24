import scapy.all as scapy
import random
import nmap
import json

def generate_random_ip():
    res = ""
    #TODO generate a random IP based on a known subnet mask
    for _ in range(4):
        res += f'{random.randint(0,255)}.'
    return res[:len(res)-1]

def search_zombies_candidate(limit=1):
    ports = [21, 22, 80, 443, 632]
    possible_candidate = set()
    
    TCP_SYN_ACK = 0x02 | 0x10
    """
    TCP Flag Values:
        SYN Flag: 0x02
        ACK Flag: 0x10
        SYN-ACK Flag: Combination of SYN and ACK, which is 0x02 | 0x10 = 0x12
    """
    
    for _ in range(limit):
        ip = generate_random_ip()
        for port in ports:
            SYN = scapy.IP(dst=ip)/scapy.TCP(dport=port, flags='S', seq=1000)
            response = scapy.sr1(SYN, timeout=4, verbose=True)
            if response is not None:
                tcp_header = response.getlayer(scapy.TCP) if response.haslayer(scapy.TCP) else None
                if tcp_header is not None and tcp_header.flags & (TCP_SYN_ACK):
                    possible_candidate.add((ip, port))
                
    
    return possible_candidate


def select_candidate(os_name: str, accuracy):
    if accuracy != "100":
        """
        TODO controlla se il timeout è di 3 volte tanto rispetto a quello delle altre macchine
        """ 
        return None
    if "Linux" not in os_name:
        return False
    try:
        linux_version = os_name.split(' ')[1]
        linux_version.split('.')
        if int(linux_version[0]) > 3:
            return False
    
        if int(linux_version[0] == 3) and int(linux_version[1] >= 3):
            return False
        
        return True
            
    except:
        return False
    

def nmap_os_detection(ip):
    nm = nmap.PortScanner()
    res = nm.scan(hosts=ip, timeout=60, arguments="-O")
    try:
        os_match = res["scan"][ip]["osmatch"][0]
        os_name = os_match["name"]
        accuracy = os_match["osclass"][0]["accuracy"]
        return select_candidate(os_name, accuracy)
    except:
        return 0
    
    
def get_zombies(candidates):
    zombies = []
    ip_found = set()
    for candidate in candidates:
        ip = candidate[0]
        port = candidate[1]
        if candidate not in ip_found:
            ip_found.add(candidate)
            if nmap_os_detection(ip):
                zombies += [{"ip": ip, "port": port}]
           
    return zombies
    
def main():
    candidates = search_zombies_candidate() 
    zombies = get_zombies(candidates)
    print(zombies)
   
            

if __name__ == "__main__":
    main()