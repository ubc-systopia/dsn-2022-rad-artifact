#!/usr/bin/bash

SCRIPT_PATH="$(cd "$(dirname $0)" && pwd)"

PROJECT_NAME="niraapad"
PROJECT_DIR=${SCRIPT_PATH}/../${PROJECT_NAME}/

python3 -m grpc_tools.protoc -I"${PROJECT_DIR}" --python_out="${PROJECT_DIR}" --grpc_python_out="${PROJECT_DIR}" "${PROJECT_DIR}"/protos/middlebox.proto
