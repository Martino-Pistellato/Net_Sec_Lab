# prepare the environment
docker system prune -a --volumes

# download image
docker pull ubuntu:22.04

# build the images and run the containers
docker compose build
docker compose up --remove-orphans