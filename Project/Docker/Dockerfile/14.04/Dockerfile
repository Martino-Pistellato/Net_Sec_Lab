# Use the Ubuntu 14.04 base image
FROM ubuntu:14.04

# Update the package list and install iproute2 and other necessary tools
RUN apt-get update && apt-get install -y iproute2 net-tools

# Add the startup script to the container
COPY Dockerfile/conf_cont.sh /usr/local/bin/conf_cont.sh

# Make the script executable
RUN chmod +x /usr/local/bin/conf_cont.sh
