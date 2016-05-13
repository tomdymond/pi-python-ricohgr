#!/usr/bin/env bash

chown -R redis:redis /var/lib/redis
chown -R appuser /var/log/piricohmoto /download

service redis-server start
service supervisor start
