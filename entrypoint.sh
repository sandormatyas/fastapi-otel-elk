#!/bin/bash
set -e

host="apm-server"
port="8200"
max_retries=30
retry_interval=5

echo "Waiting for APM server at ${host}:${port} to be ready..."
for i in $(seq 1 $max_retries); do
  if curl -s "http://${host}:${port}" > /dev/null; then
    echo "APM server is ready!"
    break
  fi
  
  if [ $i -eq $max_retries ]; then
    echo "Timeout waiting for APM server, proceeding anyway..."
  else
    echo "APM server not ready yet, retrying in ${retry_interval}s... (${i}/${max_retries})"
    sleep $retry_interval
  fi
done

poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
