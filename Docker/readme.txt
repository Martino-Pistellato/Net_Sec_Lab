### TEST NETWORK ###
This network should be used only for testing purposes. Attacker, target and zombie are on the same network without any kind of filtering. 
All container are based on Ubuntu 22.04 and the kernel version depends on the one installed in your computer. 


## SETTING UP ##
If you are running this project for the first time, you may prepare the right environment using first-setup.sh  

First-setup.sh:
- prepares the environment DELETING ALL STOPPED (and orphan) CONTAINERS, UNUSED NETWORKS, IMAGES AND VOLUMES
- downloads Ubuntu and Alpine images from Docker Hub
- builds the project
- creates networks and runs container

CAUTION! If you will edit the docker-compose.yml file or the Dockerfiles, you MUST run rebuild.sh before launch docker compose up. Otherwise, you will encounter conflicts.

Rebuild.sh:
- DELETES ALL STOPPED (and orphan) CONTAINERS, UNUSED NETWORKS, IMAGES AND VOLUMES
- builds again the project
- creates networks and runs containers