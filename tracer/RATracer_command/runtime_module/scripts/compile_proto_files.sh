#!/usr/bin/bash

SCRIPT_PATH="$(cd "$(dirname $0)" && pwd)"
CODE_DIR="${SCRIPT_PATH}/../"

#PROJECT_NAME="ratracer"
#PROJECT_DIR="${CODE_DIR}${PROJECT_NAME}/"
#PROTOS_DIR="${PROJECT_DIR}protos/"
#MIDDLEBOX_PATH="${PROTOS_DIR}ratracer.proto"

echo $CODE_DIR
#echo $PROJECT_DIR
#echo $PROTOS_DIR
#echo $MIDDLEBOX_PATH

cd "${CODE_DIR}"
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./ratracer/protos/ratracer.proto
