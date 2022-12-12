#!/bin/sh
echo "Waiting for redis..."
while ! nc -z "$FASTAPI_REDIS_HOST" "$FASTAPI_REDIS_PORT"; do
  sleep 0.1s
done
echo "Waiting for elasticsearch..."
while ! nc -z "$ES_HOST" "$ES_PORT"; do
  sleep 0.1s
done
exec "$@"
