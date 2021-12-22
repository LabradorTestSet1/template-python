#!/bin/bash

IMAGE_NAME=$(awk -F "=" '/ImageName/ {print $2}' src/config.ini)

docker build --pull --rm -f "Dockerfile" -t $IMAGE_NAME "."
