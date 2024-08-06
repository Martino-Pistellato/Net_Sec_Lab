#!/bin/sh

# Get the IP address of the eth0 interface
IP_ADDR=$(ip -4 addr show dev eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

# Extract the subnet part (first three octets)
SUBNET=$(echo $IP_ADDR | cut -d '.' -f 1-3)

# Define the new gateway IP using the extracted subnet part
NEW_GATEWAY="$SUBNET.254"

# Delete the existing default route and add the new one
ip route del default
ip route add default via $NEW_GATEWAY dev eth0

# Get the subnet from eth1 (e.g., 172.1.0.0/16)
SUBNET_ETH1=$(ip a show dev eth1 | grep 'inet' | awk '{print $2}' | cut -d '.' -f 1-3)

# Get the subnet from eth0 (e.g., 172.254.0.0/16)
# SUBNET_ETH0 = $(ip a show dev eth0 | grep 'inet' | awk '{print $2}' | cut -d '.' -f 1-3)

ip route add $SUBNET_ETH1.0/16 dev eth1 via 172.254.0.254
