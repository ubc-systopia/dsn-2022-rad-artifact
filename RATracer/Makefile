stubs:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./niraapad/protos/niraapad.proto

server:
	python3 niraapad/middlebox/start_server.py

test:
	python3 niraapad/test/test_niraapad.py
