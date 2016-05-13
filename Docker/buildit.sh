#!/usr/bin/env bash

NAME="${1}""

[ ! "${NAME}" ] && NAME="test5"

docker build -t ${NAME} .
