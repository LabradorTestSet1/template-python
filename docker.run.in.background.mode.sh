#!/bin/bash

IMAGE_NAME=$(awk -F "=" '/ImageName/ {print $2}' src/config.ini)

docker run -d \
      -v $PWD/src:/workspace/src \
      -v $PWD/log:/workspace/log \
      -v $PWD/output:/workspace/output \
      $IMAGE_NAME python src/com/iotcube/app/main.py
