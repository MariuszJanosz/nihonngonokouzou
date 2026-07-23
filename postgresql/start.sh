#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

$("${SCRIPT_DIR}/create_cluster.sh")

postgres -D "${SCRIPT_DIR}/db" >>logfile.log 2>&1 </dev/null &

