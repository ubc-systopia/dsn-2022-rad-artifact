#!/usr/bin/bash

SCRIPT_PATH="$(cd "$(dirname $0)" && pwd)"
CODE_DIR="${SCRIPT_PATH}/../"

#PROJECT_NAME="niraapad"
#PROJECT_DIR="${CODE_DIR}${PROJECT_NAME}/"
#PROTOS_DIR="${PROJECT_DIR}protos/"
#MIDDLEBOX_PATH="${PROTOS_DIR}niraapad.proto"

echo $CODE_DIR
#echo $PROJECT_DIR
#echo $PROTOS_DIR
#echo $MIDDLEBOX_PATH

cd "${CODE_DIR}"
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./niraapad/protos/niraapad.proto
