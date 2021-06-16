import inspect

from enum import Enum

FUNC_NAME = lambda: inspect.stack()[1].function
CALLER_METHOD_NAME = lambda: inspect.stack()[2].function
max_func_name_len = 100

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
    VIA_MIDDLEBOX = 2
    DIRECT_PLUS_MIDDLEBOX = 3

# Currently, we support three types of backend classes
class BACKENDS:
    SERIAL = "DirectSerial"
    UR3_ARM = "DirectUR3Arm"
    ROBOT_ARM = "DirectRobotArm"

    modules = {}

    #modules[SERIAL] = "ftdi_serial"
    #modules[UR3_ARM] = "hein_robots.universal_robots.ur3"
    #modules[ROBOT_ARM] = "hein_robots.base.robot_arms"

    modules[SERIAL] = "niraapad.backends"
    modules[UR3_ARM] = "niraapad.backends"
    modules[ROBOT_ARM] = "niraapad.backends"
