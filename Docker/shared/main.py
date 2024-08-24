import backlog, SYN_scan
import sys

def main(zombie_ip, zombie_port, target_ip):
    # backlog_size = backlog.main(zombie_ip, zombie_port)
    p_value = SYN_scan.backlog_syn_scan(128, zombie_ip, zombie_port, target_ip)
    print(p_value)
    # print(f"Target ip: {target_ip}, Backlog size: {backlog_size}, P-value: {p_value}")

if __name__ == "__main__":
    zombie_ip = sys.argv[1]
    zombie_port = int(sys.argv[2])
    target_ip = sys.argv[3]

    main(zombie_ip, zombie_port, target_ip)