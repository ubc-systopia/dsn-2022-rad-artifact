# RATracer
Prototype for the CPS security project

## Dependencies

* Python 3.7.3
* Python package grpcio 1.32.0
* Python package grpcio-tools 1.32.0
* Python package protobuf 3.15.6
* Python package tensorflow 2.4.1

The package may work with earlier versions of these depenencies, but this has not been tested.

## Styleguide

* We try to follw the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* In order to use a tool like [YAPF](https://github.com/google/yapf) (Yet Another Python Formatter) for auto-formatting:
    * Run `yapf --style google -i -r -vv files .` in the ratracer folder, or
    * Run `yapf --style google -i -vv files <filepath>` to format a specific file

## Build Steps

* Generate the gRPC stubs using one of the following methods:
    * Run `scripts/compile_proto_files.sh` script in bash
    * Run task `build` defined in `.vscode/tasks.json` in Visual Studio Code

## Testing Steps

* Test on a single machine using one of the following methods:
    * Run `.\ratracer\test\test_middlebox.py`
    * Run task `test` defined in `.vscode/tasks.json` in Visual Studio Code

* Test on two machines as follows:
    * On the server machine, run `.\ratracer\middlebox\start_server.py -P 1337 -K .\ratracer\keys\ispy\ -S`
    * On the client machine, run `.\ratracer\test\test_ratracer.py -D -H ispy -P 1337 -K .\ratracer\keys\ispy\ -S`
    * (Use `.\ratracer\middlebox\start_server.py --help` or `.\ratracer\test\test_ratracer.py --help` for details)

#### Running UR simulator

* Details on setting up UR simulator and connecting it with python script: https://github.com/ubc-systopia/cps-security-code/blob/main/docs/URsim_Setup.pdf

* Test on a single machine as follows:
    * Turn on the VMware Player and run the UR simulator virtual machine
    * Run the UR3 robot simulator and turn on the robot from the button on the bottom left
    * Run the `test_init_vm` test using `ratracer/test/test_middlebox.py`
