# Use the Ubuntu 22.04 base image
FROM ubuntu:22.04

# Update the package list and install iproute2 and other necessary tools
RUN apt-get update && apt-get install -y iproute2 net-tools iputils-ping traceroute nano

EXPOSE 8080
CMD ["/bin/bash", "-c", "sleep infinity"]