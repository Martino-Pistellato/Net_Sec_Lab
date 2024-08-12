#!/bin/sh

# Enable NAT
iptables -t nat -A POSTROUTING --out-interface eth0 -j MASQUERADE
