#!/bin/bash

export DOCKER_DEFAULT_PLATFORM=linux/amd64

export CAPTURETIME=`date +%Y-%m-%d_%H-%M-%S`
export REPNUM=$i
export DATADIR="$PWD/data"

docker-compose up -d