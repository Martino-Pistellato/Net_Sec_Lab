from scapy.all import IP, TCP, send, sniff
import logging
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_syn_packets(target_ip, target_port, num_packets):
    """
    Send SYN packets to a target to potentially fill its SYN backlog.
    
    :param target_ip: IP address of the target machine
    :param target_port: Port number on the target machine
    :param num_packets: Number of SYN packets to send
    """
    logging.info(f"Sending {num_packets} SYN packets to {target_ip}:{target_port}")
    for i in range(num_packets):
        ip = IP(dst=target_ip)
        tcp = TCP(sport=40000 + i, dport=target_port, flags='S', seq=1000 + i)
        packet = ip / tcp
        send(packet, verbose=0)
    logging.info("SYN packets sent.")

def check_eviction(target_ip, target_port, original_seq_num, original_sport):
    """
    Check whether a SYN entry has been evicted from the backlog by sending a duplicate SYN.
    
    :param target_ip: IP address of the target machine
    :param target_port: Port number on the target machine
    :param original_seq_num: Sequence number used for the original SYN
    :param original_sport: Source port used for the original SYN
    :return: 'ACK' if the original SYN is still in the backlog, 'SYN-ACK' if evicted, None if no response
    """
    # Send a duplicate SYN packet with the same sequence number and source port
    ip = IP(dst=target_ip)
    tcp = TCP(sport=original_sport, dport=target_port, flags='S', seq=original_seq_num)
    duplicate_syn = ip / tcp
    send(duplicate_syn, verbose=0)

    # Define a function to filter responses
    def syn_ack_or_ack(pkt):
        if pkt.haslayer(TCP):
            tcp_layer = pkt.getlayer(TCP)
            return (tcp_layer.dport == target_port and
                    (tcp_layer.flags & 0x12 != 0))  # SYN-ACK or ACK
        return False

    # Capture the response
    packets = sniff(filter=f'tcp and src host {target_ip} and src port {target_port}',
                    count=1, timeout=2, lfilter=syn_ack_or_ack)

    if packets:
        packet = packets[0]
        tcp_layer = packet.getlayer(TCP)
        if tcp_layer.flags & 0x10:  # ACK flag
            return 'ACK'
        elif tcp_layer.flags & 0x12:  # SYN-ACK flag
            return 'SYN-ACK'
    
    return None

def infer_backlog_size(target_ip, target_port):
    """
    Infer the SYN backlog size of a target Linux machine.

    :param target_ip: IP address of the target machine
    :param target_port: Port number on the target machine
    :return: Estimated SYN backlog size
    """
    min_backlog = 16
    max_backlog = 256
    backlog_size = min_backlog

    while backlog_size <= max_backlog:
        logging.info(f"Testing backlog size: {backlog_size}")
        
        # Send SYN packets to fill the backlog
        send_syn_packets(target_ip, target_port, int(3/4 * backlog_size))
        time.sleep(1)  # Give some time for packets to be processed

        # Check for eviction
        eviction_detected = False
        for i in range(int(3/4 * backlog_size)):
            # Use the same source port and sequence number for checking eviction
            response = check_eviction(target_ip, target_port, 1000 + i, 40000 + i)
            if response == 'SYN-ACK':
                eviction_detected = True
                break

        if eviction_detected:
            logging.info(f"Eviction detected at backlog size: {backlog_size}")
            break
        else:
            backlog_size *= 2

    if backlog_size > max_backlog:
        logging.info("Backlog size is greater than 256 or unable to determine.")
        return None
    else:
        logging.info(f"Inferred backlog size: {backlog_size}")
        return backlog_size

def main(target_ip, target_port):
    inferred_size = infer_backlog_size(target_ip, target_port)

    if inferred_size:
        print(f"Inferred SYN backlog size for {target_ip}:{target_port} is {inferred_size}.")
    else:
        print(f"Could not determine SYN backlog size for {target_ip}:{target_port}.")
        
    return inferred_size

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <target_ip> <target_port>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    main(target_ip, target_port)
