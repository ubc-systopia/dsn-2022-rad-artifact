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

        niraapad_backend_type = type.__getattribute__(
            cls, "niraapad_backend_type")
        NiraapadClient.static_setter(niraapad_backend_type, key, value)

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

class VirtualSerial(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Serial". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective origianl Serial class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.SERIAL

    @staticmethod
    def list_devices(*args, **kwargs):
        return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

    @staticmethod
    def list_device_ports(*args, **kwargs):
        return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

    @classmethod
    def list_device_serials(cls, *args, **kwargs):
        return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def open_device(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def init_device(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def update_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read_line(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def request(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def flush(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset_input_buffer(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset_output_buffer(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_bit_mode(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

DirectSerial = ftdi_serial.Serial
ftdi_serial.Serial = VirtualSerial

DirectUR3Arm = ur3.UR3Arm
ur3.UR3Arm = VirtualUR3Arm
