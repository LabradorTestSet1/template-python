FROM python:3.9-alpine

ADD src /workspace/src

RUN \
  # 1. setup build envirionment
  apk --update --no-cache add --virtual build-deps \
    git autoconf make gcc g++ automake musl-dev \
    jansson-dev yaml-dev libxml2-dev

RUN \
  mkdir -p /workspace/log && \
  cd /workspace/src && \ 
  pip install -r requirements_OnlyPython.txt && \
  apk del build-deps && \
  apk --update --no-cache add jansson yaml libxml2 libstdc++ libgcc musl git bash

WORKDIR /workspace

CMD ["python", "--help"]
