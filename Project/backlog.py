from scapy.all import IP, TCP, sr1, RandShort
import time

def send_syn_packets(target_ip, port, num_packets, rate):
    """
    Send SYN packets to the target IP and port and return responses.
    
    :param target_ip: The IP address of the target machine.
    :param port: The port to send SYN packets to.
    :param num_packets: The number of SYN packets to send.
    :param rate: The rate at which to send packets (packets per second).
    :return: List of responses.
    """
    responses = []
    for _ in range(num_packets):
        packet = IP(dst=target_ip) / TCP(dport=port, sport=RandShort(), flags="S")
        response = sr1(packet, timeout=1, verbose=0)
        if response and response.haslayer(TCP) and response[TCP].flags == "SA":
            responses.append(response)
        time.sleep(1 / rate)
    return responses

def measure_backlog_size(target_ip, ports, num_packets_per_port, rate):
    """
    Measure the SYN backlog size by sending SYN packets and observing evictions.
    
    :param target_ip: IP address of the target machine.
    :param ports: List of ports to scan.
    :param num_packets_per_port: Number of SYN packets to send per port.
    :param rate: Rate of packet sending (packets per second).
    :return: Number of packets that were evicted.
    """
    total_evicted = 0
    
    for port in ports:
        print(f"Sending SYN packets to port {port}")
        responses = send_syn_packets(target_ip, port, num_packets_per_port, rate)
        total_sent = num_packets_per_port
        total_received = len(responses)
        evicted = total_sent - total_received
        total_evicted += evicted
        
        print(f"Port {port}: Sent {total_sent}, Received {total_received}, Evicted {evicted}")
    
    print(f"Total evicted packets: {total_evicted}")
    return total_evicted


target_ip = '192.168.1.1'  # Replace with your target IP
ports = [22, 80, 443]  # Ports to send SYN packets to
num_packets_per_port = 500  # Number of SYN packets per port
rate = 2  # Rate of sending packets (2 packets per second)

evictions = measure_backlog_size(target_ip, ports, num_packets_per_port, rate)
print(f"Number of evicted packets: {evictions}")
