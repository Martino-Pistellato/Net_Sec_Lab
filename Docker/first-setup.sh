#!/bin/bash

# prepare the environment
docker system prune -a --volumes

# download all images
docker pull alpine:latest
docker pull ubuntu:12.04
docker pull ubuntu:14.04
docker pull ubuntu:16.04
docker pull ubuntu:18.04
docker pull ubuntu:20.04
docker pull ubuntu:22.04

# build the images and run the containers
docker compose build
docker compose up
