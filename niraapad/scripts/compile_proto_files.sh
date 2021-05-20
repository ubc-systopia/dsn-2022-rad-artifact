#!/usr/bin/bash

SCRIPT_PATH="$(cd "$(dirname $0)" && pwd)"

PROJECT_NAME="niraapad"
CODE_DIR="${SCRIPT_PATH}/../"
PROJECT_DIR="${CODE_DIR}${PROJECT_NAME}/"
PROTOS_DIR="${PROJECT_DIR}protos/"
MIDDLEBOX_PATH="${PROTOS_DIR}middlebox.proto"

echo $CODE_DIR
echo $PROJECT_DIR
echo $PROTOS_DIR
echo $MIDDLEBOX_PATH

cd "${CODE_DIR}"
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./niraapad/protos/middlebox.proto
# TODO Make paths above relative

#python3 -m grpc_tools.protoc -I"${PROJECT_DIR}" --python_out="${PROJECT_DIR}" --grpc_python_out="${PROJECT_DIR}" "${MIDDLEBOX_PATH}"
#python3 -m grpc_tools.protoc -I"${CODE_DIR}" --python_out="${PROTOS_DIR}" --grpc_python_out="${PROTOS_DIR}" "${MIDDLEBOX_PATH}"
