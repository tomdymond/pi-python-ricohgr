#!/usr/bin/env bash

mkdir -p /persist/redis
mkdir -p /persist/download

docker run -it --net=host \
  -v /root/config:/config \
  -v /persist/redis:/var/lib/redis \
  -v /persist/download:/download \
  --privileged \
  test5 $1
