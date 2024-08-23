FROM ubuntu:22.04

# Update the package list and install iproute2 and other necessary tools
RUN apt-get update && apt-get install -y iproute2 net-tools iputils-ping traceroute nano scapy nmap

CMD ["/bin/bash", "-c", "sleep infinity"]