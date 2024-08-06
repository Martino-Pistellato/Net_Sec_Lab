# Use a base image with FRR pre-installed
FROM frrouting/frr:latest

# Copy the FRR configuration file into the container
COPY Dockerfile/routers/main_router/frr.conf /etc/frr/frr.conf

# Expose ports for FRR (optional, for management purposes)
EXPOSE 2601 2602 2603 2604 2605

# Start FRR services
# CMD ["zebra", "bgpd", "ospfd", "ospf6d", "isisd", "ripd", "ripngd", "pimd", "ldpd", "nhrpd", "eigrpd", "bfdd", "vrrpd"]
CMD ["zebra"]
