# Use the Ubuntu 12.04 base image
FROM ubuntu:12.04

# Copy packages to the container
COPY Dockerfile/hosts/corpB/12.04/iproute.deb /usr/local/bin/iproute.deb
COPY Dockerfile/hosts/corpB/12.04/net-tools.deb /usr/local/bin/net-tools.deb
COPY Dockerfile/hosts/corpB/12.04/traceroute.deb /usr/local/bin/traceroute.deb

# Install packages
RUN dpkg -i /usr/local/bin/net-tools.deb
RUN dpkg -i /usr/local/bin/iproute.deb
RUN dpkg -i /usr/local/bin/traceroute.deb

# Clean up
RUN rm /usr/local/bin/net-tools.deb
RUN rm /usr/local/bin/iproute.deb
RUN rm /usr/local/bin/traceroute.deb

# Add the startup script to the container
COPY Dockerfile/hosts/corpB/conf_cont.sh /usr/local/bin/conf_cont.sh

# Make the script executable
RUN chmod +x /usr/local/bin/conf_cont.sh

CMD ["/bin/bash", "-c", "/usr/local/bin/conf_cont.sh && sleep infinity"]
