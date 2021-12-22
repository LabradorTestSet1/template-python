#!/bin/bash

IMAGE_NAME=$(awk -F "=" '/ImageName/ {print $2}' src/config.ini)

docker run -it --rm \
      -v $PWD/src:/workspace/src \
      -v $PWD/log:/workspace/log \
      -v $PWD/output:/workspace/output \
      $IMAGE_NAME /bin/bash
