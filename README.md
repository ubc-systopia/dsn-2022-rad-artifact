# Niraapad
Prototype for the CPS security project

## Dependencies

* Python 3.7.3
* Python package grpcio 1.32.0
* Python package grpcio-tools 1.32.0
* Python package protobuf 3.15.6
* Python package tensorflow 2.4.1

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

## Distribution

* To distribute the `niraapad` package on Python Package Index:
    * Clean all old files related to distribution using `rm -rf build/ dist/ *egg*`
    * Update the version info in file `__version__.py`
    * Generate the distribution package using `python3 setup.py sdist bdist_wheel`
    * Run `twine check dist/*` to check for errors and warnings
    * If you want to test the final package, upload it first to TestPyPI server using `twine upload --repository testpypi dist/*`
    * The package can be installed from TestPyPI server using `pip install -i https://test.pypi.org/simple/ niraapad==1.1.0`
    * After the package is tested, upload it to the PyPI server using `twine upload dist/*`

* Currently, Arpan Gujarati is the sole owner and maintainer of the `niraapad` package on Python Package Index
