
If you are running this project for the first time, you may prepare the right environment using first-setup.sh  

First-setup.sh:
- prepares the environment DELETING ALL STOPPED CONTAINERS, UNUSED NETWORKS, IMAGES AND VOLUMES
- downloads Ubuntu and Alpine images from Docker Hub
- builds the project
- creates networks and runs container

CAUTION! If you will edit the docker-compose.yml file or the Dockerfiles, you MUST run rebuild.sh before launch docker compose up. Otherwise, you will encounter conflicts.

Rebuild.sh:
- DELETES ALL STOPPED CONTAINERS, UNUSED NETWORKS, IMAGES AND VOLUMES
- builds again the project
- creates networks and runs containers

