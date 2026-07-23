#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

$("${SCRIPT_DIR}/start.sh")

RETRIES=5

until psql -c 'SELECT 1' postgres >/dev/null 2>&1 || [ ${RETRIES} -le 0 ] ; do
	RETRIES=$((${RETRIES}-1))
	sleep 1
done

psql -f "${SCRIPT_DIR}/000.sql" postgres

