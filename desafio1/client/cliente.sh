#!/bin/bash
# O nome 'app' é como o container do servidor será acessado na rede Docker
SERVER_HOST="app"
SERVER_PORT="8080"
URL="http://${SERVER_HOST}:${SERVER_PORT}"

echo "Iniciando requisições periódicas para: ${URL}"

while true; do
  echo "--------------------------------------------------"
  echo "Tentando requisição em $(date '+%H:%M:%S')..."
  curl -s -w "\nStatus: %{http_code}\nTempo Total: %{time_total}s\n" $URL
  echo "--------------------------------------------------"
  sleep 5
done