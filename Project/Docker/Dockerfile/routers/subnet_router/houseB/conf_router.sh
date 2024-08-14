#!/bin/sh

# Get the IP address of the eth0 interface
IP_ADDR=$(ip -4 addr show dev eth0 | grep -Eo 'inet [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | awk '{print $2}')

# Extract the subnet part (first three octets)
SUBNET=$(echo $IP_ADDR | cut -d '.' -f 1-3)

# Define the new gateway IP using the extracted subnet part
NEW_GATEWAY="$SUBNET.77"

# Delete the existing default route and add the new one
ip route del default
ip route add default via $NEW_GATEWAY dev eth0

# Enable NAT
iptables -t nat -A POSTROUTING --out-interface eth0 -j MASQUERADE

#Enable port forwarding
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8082 -j DNAT --to-destination 192.168.2.3:8082
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
#sh -c "iptables-save > /etc/iptables/rules.v4"