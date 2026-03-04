#!/bin/sh

if [ -s /env-mount/env.sh ]; then
  echo "Sourcing env.sh"
  . /env-mount/env.sh
else
  echo "env.sh missing or empty"
fi

# Create output directories in writable /tmp location
mkdir -p /tmp/outputs /tmp/logs
chmod 755 /tmp/outputs /tmp/logs

if [ -d "$KIT_INPUTS_FILE" ]; then
  echo "Found input file, processing…"
else
  echo "No input file supplied, continuing without it"
fi

exec "$@"
