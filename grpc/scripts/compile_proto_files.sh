#!/usr/bin/bash

SCRIPT_PATH="$(cd "$(dirname $0)" && pwd)"

GRPC_DIR=${SCRIPT_PATH}/../
PROTO_INPUT_DIR=${GRPC_DIR}protos/
PROTO_OUTPUT_DIR=${GRPC_DIR}gen/

mkdir -p "${PROTO_OUTPUT_DIR}"

python3 -m grpc_tools.protoc -I"${PROTO_INPUT_DIR}" --python_out="${PROTO_OUTPUT_DIR}" --grpc_python_out="${PROTO_OUTPUT_DIR}" "${PROTO_INPUT_DIR}"/middlebox.proto
