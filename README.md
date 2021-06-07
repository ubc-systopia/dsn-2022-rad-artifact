# cps-security-code
Prototyping for the CPS security project

## gRPC

Currently working with the following versions: Python 3.7.3 and libprotoc (grpc_tools.protoc) 3.15.2.

From my past experience, protocol buffers can be very sensitive to version changes!

Testing steps:

Add the `niraapad` folder in the top-level directory to your PYTHONPATH environment variable.

#### Linux:
* Compile the protocol buffer IDL files by running the  `compile_proto_files.sh` bash script, which is located in `niraapad/script`
* Run tests using `python3 niraapad/test/test_middlebox.py`

#### Windows:
* Compile the protocol buffer IDL files by running the  `compile_proto_files_w.sh` bash script, which is located in `niraapad/script`
* Run tests using `python niraapad/test/test_middlebox.py`

#### Visual Studio Code on Windows (tested on `ispy`):
* The `.vscode` folder contains the necessary configuration files
* Run the `build` task to compile  the protocol buffer IDL files
* Run the `test` task to run `test_middlebox.py`

### UPDATED Dependencies
* Updating protocol buffer, grpcio, and grpcio-tools versions to 3.5.1, 1.9.0, and 1.9.0, respectively
* https://gitlab.com/heingroup/hein_robots
* https://github.com/SintefManufacturing/python-urx
