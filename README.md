# cps-security-code
Prototyping for the CPS security project

## gRPC

Currently working with the following versions: Python 3.7.3 and libprotoc (grpc_tools.protoc) 3.15.2.

From my past experience, protocol buffers can be very sensitive to version changes!

Add the `niraapad` folder in the top-level directory to your PYTHONPATH environment variable.

Testing steps:

##### Linux:
* Compile the protcol buffer IDL files by running the  `compile_proto_files.sh` bash script, which is located in `niraapad/script`
* Run tests using `python3 niraapad/test/test_middlebox.py`

##### Windows:
* Compile the protcol buffer IDL files by running the  `compile_proto_files_w.sh` bash script, which is located in `niraapad/script`
* Run tests using `python niraapad/test/test_middlebox.py`
