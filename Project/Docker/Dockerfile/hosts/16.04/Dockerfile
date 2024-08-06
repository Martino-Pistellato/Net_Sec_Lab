# Use the Ubuntu 16.04 base image
FROM ubuntu:16.04


### The following snippet installs packets for classic routing (that is not working)
# Update the package list and install iproute2 and other necessary tools
RUN apt-get update && apt-get install -y iproute2 net-tools

# Add the startup script to the container
COPY Dockerfile/hosts/conf_cont.sh /usr/local/bin/conf_cont.sh

# Make the script executable
RUN chmod +x /usr/local/bin/conf_cont.sh

###

### Install prerequistes, add repo for bird2 an install it
RUN apt-get update && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:cz.nic-labs/bird && \
    apt-get update

RUN apt-get install -y bird2




