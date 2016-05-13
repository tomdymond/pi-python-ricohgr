#!/usr/bin/env bash

NAME="${1}"

[ ! "${NAME}" ] && NAME="test5"

COMMAND=$1

mkdir -p /persist/${NAME}/{redis,download,logs}

docker run -it --net=host \
  -v /root/config:/config \
  -v /persist/${NAME}/redis:/var/lib/redis \
  -v /persist/${NAME}/download:/download \
  -v /persist/${NAME}/logs:/var/log/piricohmoto \
  --privileged \
  ${NAME} ${COMMAND}
