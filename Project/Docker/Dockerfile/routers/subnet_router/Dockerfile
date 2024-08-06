# Use the Ubuntu 22.04 image
FROM ubuntu:22.04

# Update the package list and install iproute2 and other necessary tools
RUN apt-get update && apt-get install -y iproute2 net-tools

# Add the startup script to the container
COPY Dockerfile/routers/subnet_router/add_route.sh /usr/local/bin/add_route.sh

# Make the script executable
RUN chmod +x /usr/local/bin/add_route.sh
