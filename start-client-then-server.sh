#!/bin/bash

set -e

_script_dir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

# Trap SIGINT (CTRL+C) and kill both processes before exiting.
trap 'echo "Terminating processes..."; kill $CLIENT_PID $SERVER_PID 2>/dev/null; exit 0' SIGINT

export GRPC_LOG_FOLDER="${_script_dir}/_logs"
mkdir -p ${GRPC_LOG_FOLDER}

export GRPC_CLIENT_LOG_FILE="${GRPC_LOG_FOLDER}/client.log"
echo "Redirecting client gRPC logs to $GRPC_CLIENT_LOG_FILE"

export GRPC_SERVER_LOG_FILE="${GRPC_LOG_FOLDER}/server.log"
echo "Redirecting client gRPC logs to $GRPC_SERVER_LOG_FILE"

export GRPC_TRACE=http_keepalive,health_check_client,client_channel 

echo "Starting client..."
# Start the client in the background with GRPC trace enabled.
poetry run python client.py 2>${GRPC_CLIENT_LOG_FILE} &
CLIENT_PID=$!

echo "Waiting 5 seconds before starting server..."
echo "The client will immediately try to connect to the server,"
echo "but it will not fail because of the waitForReady in the config.json"
sleep 5

echo "Starting server..."
# Start the server in the background with GRPC trace enabled.
poetry run python server.py 2>${GRPC_SERVER_LOG_FILE} &
SERVER_PID=$!

echo "Press CTRL+C to exit"

# Wait for both background processes to finish.
wait $CLIENT_PID $SERVER_PID
