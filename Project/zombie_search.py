import scapy.all as scapy
import random
import nmap
import json

def search_zombie():
    pass 

def generate_random_ip():
    res = ""
    #TODO generate a random IP based on a known subnet mask
    for _ in range(4):
        res += f'{random.randint(0,255)}.'
    return res[:len(res)-1]

def search_zombies_illegal(limit=1):
    # ports = [21, 22, 80, 443, 632]
    ports = [80]
    possible_candidate = set()
    
    TCP_SYN_ACK = 0x02 | 0x10
    """
    TCP Flag Values:
        SYN Flag: 0x02
        ACK Flag: 0x10
        SYN-ACK Flag: Combination of SYN and ACK, which is 0x02 | 0x10 = 0x12
    """
    
    for _ in range(limit):
        # ip = generate_random_ip()
        ip = "45.33.32.156" 
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
        return 0
    if "Linux" not in os_name:
        return 0
    try:
        # non ho ben capito, dicono che prendono versioni di linux sotto alla 3.3, ma poi dicono che hanno fatto "finerprint" su versioni di linux sotto alla 3.0, ma quindi le 3.1 e 3.2 vengono prese o no?
        linux_version = os_name.split(' ')[1]
        linux_version.split('.')
        if int(linux_version[0]) <= 2:
            return 2
        if int(linux_version[0]) > 3:
            return 0 
        if int(linux_version[1]) >= 3:
            return 0 
        
        if int(linux_version[1]) == 0:
            return 2
        
       
        return 1
        
        
    except:
        return 0
    

def nmap_os_detection(ip):
    nm = nmap.PortScanner()
    res = nm.scan(hosts=ip, timeout=60, arguments="-O")
    # with open("res.json", 'w') as f:
    #     json.dump(res,f)
    try:
        os_match = res["scan"][ip]["osmatch"][0]
        os_name = os_match["name"]
        accuracy = os_match["osclass"][0]["accuracy"]
        print(os_name)
        print(accuracy)

        return select_candidate(os_name, accuracy)
    except:
        return 0
    
    
def get_zombies(candidates):
    zombies = []
    ip_found = set()
    for candidate in candidates:
        if candidate[0] in ip_found:
            continue 
        ip_found.add(candidate[0])
        if res := nmap_os_detection(candidate[0]):
            zombies += [{"ip": candidate[0], "tested_port": candidate[1], "fingerprint": True if res == 2 else False}] if res != 0 else []
           
    return zombies
    
def main():
    candidates = search_zombies_illegal() 
    """
    45.33.32.156 is scanme.nmap.org, you can scan it, idk ab
    """
    zombies = get_zombies(candidates)
    print(zombies)
   
            

if __name__ == "__main__":
    main()