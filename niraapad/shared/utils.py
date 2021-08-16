import os
import sys
import pickle
import inspect

from enum import Enum
from copy import copy

from ftdi_serial import FtdiDevice, SerialDeviceInfo

FUNC_NAME = lambda: inspect.stack()[1].function
CALLER_METHOD_NAME = lambda: inspect.stack()[2].function
max_func_name_len = 100


# Disable print() output
def disable_print():
    sys.stdout = open(os.devnull, 'w')


# Restore print() output
def enable_print():
    sys.stdout = sys.__stdout__


def sanitize_resp(name, resp):
    # TODO: Get rid of this!!!
    # The following is a work around to circumvent the problem
    # with pickling ctypes objects containing pointers,
    # like instances of ftdi_serial.SerialDeviceInfo class.
    # It seems the easiest way to get rid of this work around
    # is to upgrade to the latest version of ftdi_serial.

    # Parameter name refers to the method or the property name

    new_resp = copy(resp)

    try:
        pickled_resp = pickle.dumps(new_resp)
    except ValueError as e:
        if name == "list_devices":
            assert (type(new_resp) == list)
            for i in range(0, len(new_resp)):
                assert (type(new_resp[i]) == SerialDeviceInfo)
                new_resp[i].handle = None
        elif name == "device":
            assert (type(new_resp) == FtdiDevice)
            if hasattr(new_resp, 'ftdi'):
                new_resp.ftdi = None
    return new_resp


# We define three different mode of operation (MOs)..
#
# Mode 1, DIRECT: This is the coventional mode, where requests are
# sent directly to the C9 and to other robot modules via serial communication
# (nothing really changes in this case).
#
# Mode 2, VIA_MIDDLEBOX: This is the mode that we eventually want, where
# requests are sent directly to the Middlebox over Ethernet, which in turn
# forwards them to the C9 and to other robot modules via serial communication
# (note that in this case, all modules are physically connected to the Middlebox
# and not to the Lab Computer).
#
# MOde 3, DIRECT_PLUS_MIDDLEBOX: This is a temporary mode,
# where are sent directly to the C9 and to other robot modules via serial
# communication and the response is also fetched likewise, but at the same time
# all the requests and all the responses are also forwarded to the Middlebox
# for tracing purposes. This design also demonstrates that the version of
# "class Serial", which we define below, works seamlessely with the rest of the
# experiment scripts from Hein Lab and NOrth Robotics.


class MO(Enum):
    DIRECT = 1
    DIRECT_PLUS_MIDDLEBOX = 2
    VIA_MIDDLEBOX = 3


# Currently, we support only the selected types of backend classes
class BACKENDS:
    DEVICE = "Directevice"
    MOCK_DEVICE = "DirectMockDevice"
    FTDI_DEVICE = "DirectFtdiDevice"
    PY_SERIAL_DEVICE = "DirectPySerialDevice"
    UR3_ARM = "DirectUR3Arm"
    ROBOT_ARM = "DirectRobotArm"
