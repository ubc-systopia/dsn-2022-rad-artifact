# Niraapad
Prototype for the CPS security project

## Dependencies

* Python 3.7.3
* Python package grpcio 1.38.0
* Python package grpcio-tools 1.38.0
* Python package protobuf 3.17.3

The package may work with earlier versions of these depenencies, but this has not been tested.

## Build Steps

* Generate the gRPC stubs using one of the following methods:
    * Run `scripts/compile_proto_files.sh` script in bash
    * Run task `build` defined in `.vscode/tasks.json` in Visual Studio Code

## Testing Steps

* Test on a single machine using one of the following methods:
    * Run `.\niraapad\test\test_middlebox.py`
    * Run task `test` defined in `.vscode/tasks.json` in Visual Studio Code

* Test on two machines as follows:
    * On the server machine, run `.\niraapad\middlebox\start_server.py -P 1337 -K .\niraapad\keys\ispy_cs_ubc_ca\ -S`
    * On the client machine, run `.\niraapad\test\test_niraapad.py -D -H ispy.cs.ubc.ca -P 1337 -K .\niraapad\keys\ispy_cs_ubc_ca\ -S`
    * (Use `.\niraapad\middlebox\start_server.py --help` or `.\niraapad\test\test_niraapad.py --help` for details)

#### Running UR simulator

* Test on a single machine as follows:
    * Turn on the VMware Player and run the UR simulator virtual machine
    * Run the UR3 robot simulator and turn on the robot from the button on the bottom left
    * Run the `test_init_vm` test using `niraapad/test/test_middlebox.py`

* Test on two machines as follows:
    * TODO
