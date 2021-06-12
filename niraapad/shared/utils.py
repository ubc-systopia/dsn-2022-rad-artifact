import inspect

from enum import Enum

FUNC_NAME = lambda: inspect.stack()[1].function
CALLER_METHOD_NAME = lambda: inspect.stack()[2].function
max_func_name_len = 100

def generate_init_call_string(class_name, arg_names, positional_args,
                              keyword_args):
    init_call_string = class_name + "("

    for i in range(0, len(positional_args)):
        init_call_string += "args[" + str(i) + "], "

    for arg_name in arg_names:
        if arg_name == "self": continue
        if arg_name in keyword_args:
            init_call_string += arg_name + "=kwargs['" + arg_name + "'], " 

    init_call_string += ")"
    return init_call_string

def generate_method_call_string(class_obj_name, class_func_name, func_arg_names,
                                positional_args, keyword_args):
    method_call_string = ""
    if class_obj_name != None: method_call_string += class_obj_name + "."
    method_call_string += class_func_name + "("

    for i in range(0, len(positional_args)):
        method_call_string += "args[" + str(i) + "], "

    for arg_name in func_arg_names:
        if arg_name == "self": continue
        if arg_name in keyword_args:
            method_call_string += arg_name + "=kwargs['" + arg_name + "'], " 

    method_call_string += ")"
    return method_call_string

def generate_getter_call_string(class_obj_name, class_prop_name):
    getter_call_string = ""
    if class_obj_name != None: getter_call_string += class_obj_name + "."
    getter_call_string += class_prop_name
    return getter_call_string

def generate_setter_call_string(class_obj_name, class_prop_name):
    setter_call_string = ""
    if class_obj_name != None: setter_call_string += class_obj_name + "."
    setter_call_string += class_prop_name + " = value"
    return setter_call_string

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

BACKEND_SERIAL = "DirectSerial"
BACKEND_UR3_ARM = "DirectUR3Arm"
BACKEND_ROBOT_ARM = "DirectRobotArm"