# Use a base image with FRR pre-installed
FROM frrouting/frr:latest

# Copy the FRR configuration file into the container
COPY Dockerfile/routers/subnet_router/houseA/frr.conf /etc/frr/frr.conf
COPY Dockerfile/routers/subnet_router/conf_router.sh /usr/local/bin/conf_router.sh

# Configure permissions
RUN chmod +x /usr/local/bin/conf_router.sh

# Run configuration script and sleep
CMD ["/bin/bash", "-c", "/usr/local/bin/conf_router.sh && sleep infinity"]
