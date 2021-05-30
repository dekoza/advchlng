#!/usr/bin/env bash

set -o errexit
set -o pipefail
cmd="$@"

/wait-for-it.sh ${POSTGRES_HOST}:${POSTGRES_PORT} -t 120

exec $cmd
