#!/usr/bin/env bash

CONTAINER="test5"
COMMAND=$1

mkdir -p /persist/${CONTAINER}/redis
mkdir -p /persist/${CONTAINER}/download
mkdir -p /persist/${CONTAINER}/logs

docker run -it --net=host \
  -v /root/config:/config \
  -v /persist/${CONTAINER}/redis:/var/lib/redis \
  -v /persist/${CONTAINER}/download:/download \
  -v /persist/${CONTAINER}/logs:/var/log/piricohmoto
  --privileged \
  ${CONTAINER} ${COMMAND}
