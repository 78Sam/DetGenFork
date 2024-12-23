#!/bin/bash

DURATION="$1"
export CONCURRENT_THREADS="$2"
export REQUESTS="$3"
export CAPTURETIME=`date +%Y-%m-%d_%H-%M-%S`
export SCENARIO="1"
REPEAT="$4"


[ -z "$DURATION" ] && DURATION=60
[ -z "$REPEAT" ] && REPEAT=1
[ -z "$CONCURRENT_THREADS" ] && CONCURRENT_THREADS=10
[ -z "$REQUESTS" ] && REQUESTS=2000

function bringup {
    echo "Start the containerised applications..."
    export DATADIR="$PWD/data"
    docker compose --ansi NEVER up -d
}

function teardown {
    echo "Take down the containerised applications and networks..."
    # NB: this removes everything so it is hard to debug from this script
    # TODO: add a `--debug` option instead use `docker-compose stop`.
    docker compose --ansi NEVER down -v
    echo "Done."
}

trap '{ echo "Interrupted."; teardown; exit 1; }' INT

for ((i=1; i<=REPEAT; i++))
do
    echo "Repeat Nr " $i
    export REPNUM=$i
    bringup;
    echo "Capturing data now for $DURATION seconds...."
    sleep $DURATION
    teardown;
done

