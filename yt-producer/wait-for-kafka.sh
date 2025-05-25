#!/bin/bash
# wait-for-kafka.sh

echo "Esperando a que Kafka esté disponible..."
until nc -z -v -w30 kafka 9092
do
  echo "Esperando..."
  sleep 5
done
echo "Kafka está disponible."
exec "$@"