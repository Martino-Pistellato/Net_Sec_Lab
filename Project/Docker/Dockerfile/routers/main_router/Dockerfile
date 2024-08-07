# Use a base image with FRR pre-installed
FROM frrouting/frr:latest

# Copy the FRR configuration file into the container
COPY Dockerfile/routers/main_router/frr.conf /etc/frr/frr.conf
COPY Dockerfile/routers/main_router/enable_nat.sh /usr/local/bin/enable_nat.sh

# Configure permissions
RUN chmod +x /usr/local/bin/enable_nat.sh

# Run configuration script and sleep
CMD ["/bin/bash", "-c", "/usr/local/bin/enable_nat.sh && sleep infinity"]
