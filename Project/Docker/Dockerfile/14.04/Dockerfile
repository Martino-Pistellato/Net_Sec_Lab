###THIS DOCKERFILE IT'S A MESS. PLEASE DON'T USE IT. I'M STILL WORKING ON IT###



# Use the Ubuntu 14.04 base image
FROM ubuntu:14.04

# Update package list and install prerequisites
# RUN apt-get update && \
#     apt-get install -y unzip gcc binutils m4 make iputils-ping flex bision build-essential libncurses5-dev libncursesw5-dev libreadline6 libreadline6-dev git && \
#     rm -rf /var/lib/apt/lists/*


RUN apt-get update && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:cz.nic-labs/bird && \
    apt-get update
# Add the startup script to the container
COPY Dockerfile/conf_cont.sh /usr/local/bin/conf_cont.sh

# Make the script executable
RUN chmod +x /usr/local/bin/conf_cont.sh
