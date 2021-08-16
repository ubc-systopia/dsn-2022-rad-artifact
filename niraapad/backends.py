import os
import sys

import niraapad.shared.utils as utils
from niraapad.lab_computer.niraapad_client import NiraapadClient

import ftdi_serial
from hein_robots.universal_robots import ur3
from hein_robots.base import robot_arms


class AttributeMeta(type):

    def __getattribute__(cls, key):
        """
        This function overrides the object.__getattribute__ method and is used
        trap and appropriately handle all read accesses to class variables.
        """

        try:
            return type.__getattribute__(cls, key)
        except AttributeError:
            niraapad_backend_type = type.__getattribute__(
                cls, "niraapad_backend_type")
            return NiraapadClient.static_getter(niraapad_backend_type, key)

    def __setattr__(cls, key, value):
        """
        This function overrides the type.__setattr__ method and is used to
        trap and appropriately handle all write accesses to class variables.
        """

        niraapad_backend_type = type.__getattribute__(cls,
                                                      "niraapad_backend_type")
        NiraapadClient.static_setter(niraapad_backend_type, key, value)


# Ignoring class ftdi_serial.Serial because we have
# decided to virtualize the Device classes instead,
# which actually are closer to the network layer

# class VirtualSerial(NiraapadClient, metaclass=AttributeMeta):
#     """
#     This class is just a facade. It's objective is to provide the same
#     interface to all Hein Lab experiment scripts as the erstwhile "class
#     Serial". In addition, the class maintains three operation modes as
#     summarized above along in "class MO". In order to do so, this class simply
#     forwards each function call to the respective function call in the
#     respective origianl Serial class object (class objects are not involved in
#     the case of static functions), or to the respective function call in the
#     global object of type "class NiraapadClientHelper" (which in turn invokes
#     an RPC to the middlebox), or both.
#     """

#     niraapad_backend_type = utils.BACKENDS.SERIAL
#     niraapad_access_variable = ""

#     @staticmethod
#     def list_devices(*args, **kwargs):
#         return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

#     @staticmethod
#     def list_device_ports(*args, **kwargs):
#         return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

#     @classmethod
#     def list_device_serials(cls, *args, **kwargs):
#         return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

#     def __init__(self, *args, **kwargs):
#         return self.initialize(*args, **kwargs)

#     def open_device(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def connect(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def disconnect(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def init_device(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def set_parameters(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def update_timeouts(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def read(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def read_line(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def write(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def request(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def flush(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def reset_input_buffer(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def reset_output_buffer(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def set_bit_mode(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)


class VirtualDevice(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Device". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original Device class object (class objects are not involved
    in the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.DEVICE
    niraapad_access_variable = ""  #"device"

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def add_write_handler(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def purge(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_baud_rate(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_input_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_output_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read_all(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def enable_write_log(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_write_log(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear_write_log(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_bit_mode(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


# Among all the Device subclasses,
# supporting classes FtdiDevice and PySerialDevice,
# but ignoring class ftdi_serial.MockDevice,
# because it is not supported in ftdi-serial v0.1.9

# class VirtualMockDevice(VirtualDevice, metaclass=AttributeMeta):
#     """
#     This class is just a facade. It's objective is to provide the same
#     interface to all Hein Lab experiment scripts as the erstwhile "class
#     MockDevice". In addition, the class maintains three operation modes as
#     summarized above along in "class MO". In order to do so, this class simply
#     forwards each function call to the respective function call in the
#     respective original MockDevice class object (class objects are not involved in
#     the case of static functions), or to the respective function call in the
#     global object of type "class NiraapadClientHelper" (which in turn invokes
#     an RPC to the middlebox), or both.
#     """

#     niraapad_backend_type = utils.BACKENDS.MOCK_DEVICE
#     niraapad_access_variable = "" #"device"

#     def __init__(self, *args, **kwargs):
#         return self.initialize(*args, **kwargs)

#     def close(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def clear(self, *args, **kwargs)
#         return self.generic_method(*args, **kwargs)

#     def get_input_size(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def write(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def read(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)


class VirtualFtdiDevice(VirtualDevice, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    FtdiDevice". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original FtdiDevice class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.FTDI_DEVICE
    niraapad_access_variable = ""  #"device"

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_baud_rate(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_input_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_output_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_bit_mode(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualPySerialDevice(VirtualDevice, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    PySerialDevice". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original PySerialDevice class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.PY_SERIAL_DEVICE
    niraapad_access_variable = ""  #"device"

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_baud_rate(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_input_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_output_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualRobotArm(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    RobotArm". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original RobotArm class object (class objects are not involved
    in the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.ROBOT_ARM
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def pause(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def resume(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def emergency_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear_faults(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def home(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_tool(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_to_location(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_tool_to_location(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_to_locations(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_tool_to_locations(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_joints(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_joint(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_twist(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_twist_to(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for_gripper_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def open_gripper(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def close_gripper(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualUR3Arm(VirtualRobotArm, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    UR3Arm". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original UR3Arm class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.UR3_ARM
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def emergency_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_to_location(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_joints(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_circular(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for_gripper_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def open_gripper(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


# ===== THESE ARE IMPORTANT FOR MONKEY PATCHING =====
# Ignoring class ftdi_serial.Serial because we have
# decided to virtualize the Device classes instead,
# which actually are closer to the network layer
# DirectSerial = ftdi_serial.Serial
# ftdi_serial.Serial = VirtualSerial

# # Among all the Device subclasses,
# # supporting classes FtdiDevice and PySerialDevice,
# # but ignoring class ftdi_serial.MockDevice,
# # because it is not supported in ftdi-serial v0.1.9
# DirectMockDevice = ftdi_serial.MockDevice
# ftdi_serial.MockDevice = VirtualMockDevice

DirectFtdiDevice = ftdi_serial.FtdiDevice
ftdi_serial.FtdiDevice = VirtualFtdiDevice

DirectPySerialDevice = ftdi_serial.PySerialDevice
ftdi_serial.PySerialDevice = VirtualPySerialDevice

# The UR3Arm does not directly rely on the Device
# classes (i.e., serial communication) but instead
# communicates with the lab computer over LAN
DirectUR3Arm = ur3.UR3Arm
ur3.UR3Arm = VirtualUR3Arm
# ===================================================
