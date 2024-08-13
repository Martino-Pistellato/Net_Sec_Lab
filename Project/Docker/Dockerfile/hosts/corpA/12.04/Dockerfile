# Use the Ubuntu 12.04 base image
FROM ubuntu:12.04

# Copy packages to the container
COPY Dockerfile/hosts/corpA/12.04/iproute_20111117-1ubuntu2_amd64.deb /usr/local/bin/iproute_20111117-1ubuntu2_amd64.deb
COPY Dockerfile/hosts/corpA/12.04/net-tools_1.60-24.2ubuntu1_amd64.deb /usr/local/bin/net-tools_1.60-24.2ubuntu1_amd64.deb
COPY Dockerfile/hosts/corpA/12.04/traceroute.deb /usr/local/bin/traceroute.deb
COPY Dockerfile/hosts/corpA/12.04/netcat.deb /usr/local/bin/netcat.deb

# Install packages
RUN dpkg -i /usr/local/bin/net-tools_1.60-24.2ubuntu1_amd64.deb
RUN dpkg -i /usr/local/bin/iproute_20111117-1ubuntu2_amd64.deb
RUN dpkg -i /usr/local/bin/traceroute.deb
RUN dpkg -i /usr/local/bin/netcat.deb

# Clean up
RUN rm /usr/local/bin/net-tools_1.60-24.2ubuntu1_amd64.deb
RUN rm /usr/local/bin/iproute_20111117-1ubuntu2_amd64.deb
RUN rm /usr/local/bin/traceroute.deb
RUN rm /usr/local/bin/netcat.deb

# Add the startup script to the container
COPY Dockerfile/hosts/corpA/conf_cont.sh /usr/local/bin/conf_cont.sh

# Make the script executable
RUN chmod +x /usr/local/bin/conf_cont.sh

CMD ["/bin/bash", "-c", "/usr/local/bin/conf_cont.sh && nc -l 80 && sleep infinity"]
