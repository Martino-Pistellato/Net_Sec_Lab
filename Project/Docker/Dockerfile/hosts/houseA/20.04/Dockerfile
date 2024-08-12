# Use the Ubuntu 20.04 base image
FROM ubuntu:20.04

# Update the package list and install iproute2 and other necessary tools
RUN apt-get update && apt-get install -y iproute2 net-tools iputils-ping traceroute nano

# Add the startup script to the container
COPY Dockerfile/hosts/houseA/conf_cont.sh /usr/local/bin/conf_cont.sh

# Make the script executable
RUN chmod +x /usr/local/bin/conf_cont.sh

CMD ["/bin/bash", "-c", "/usr/local/bin/conf_cont.sh && sleep infinity"]
