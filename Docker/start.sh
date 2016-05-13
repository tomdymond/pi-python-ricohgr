#!/usr/bin/env bash

chown -R redis:redis /var/lib/redis

service redis-server start
service supervisor start
