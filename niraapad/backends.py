import os
import sys

import niraapad.shared.utils as utils
from niraapad.lab_computer.niraapad_client import NiraapadClient

import ftdi_serial
from hein_robots.universal_robots import ur3
from hein_robots.base import robot_arms

class VirtualRobotArm(NiraapadClient):
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

    backend_type = utils.BACKENDS.ROBOT_ARM

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    @property
    def connected(self):
        return self.generic_getter()

    @property
    def max_velocity(self):
        return self.generic_getter()

    @max_velocity.setter
    def max_velocity(self, value):
        return self.generic_setter(value)

    @property
    def default_velocity(self):
        return self.generic_getter()

    @default_velocity.setter
    def default_velocity(self, value):
        return self.generic_setter(value)

    @property
    def acceleration(self):
        return self.generic_getter()

    @property
    def velocity(self):
        return self.generic_getter()

    @property
    def location(self):
        return self.generic_getter()

    @property
    def twist(self):
        return self.generic_getter()

    @property
    def wrench(self):
        return self.generic_getter()

    @property
    def joint_positions(self):
        return self.generic_getter()

    @property
    def joint_count(self):
        return self.generic_getter()

    @property
    def gripper_position(self):
        return self.generic_getter()

    @property
    def gripper_velocity(self):
        return self.generic_getter()

    @property
    def gripper_default_velocity(self):
        return self.generic_getter()

    @gripper_default_velocity.setter
    def gripper_default_velocity(self, velocity):
        return self.generic_setter(value)

    @property
    def gripper_default_force(self):
        return self.generic_getter()

    @gripper_default_force.setter
    def gripper_default_force(self, force):
        return self.generic_setter(value)

    @property
    def tool_offset(self):
        return self.generic_getter()

    @tool_offset.setter
    def tool_offset(self):
        return self.generic_setter(value)

    @property
    def tool_mass(self):
        return self.generic_getter()

    @tool_mass.setter
    def tool_mass(self, value):
        return self.generic_setter(value)

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

class VirtualUR3Arm(VirtualRobotArm):
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

    backend_type = utils.BACKENDS.UR3_ARM

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    @property
    def robot(self):
        return self.generic_getter()

    @property
    def connected(self):
        return self.generic_getter()

    @property
    def default_joint_velocity(self):
        return self.generic_getter()

    @default_joint_velocity.setter
    def default_joint_velocity(self, value):
        return self.generic_setter(value)

    @property
    def acceleration(self):
        return self.generic_getter()

    @property
    def velocity(self):
        return self.generic_getter()

    @property
    def pose(self):
        return self.generic_getter()

    @property
    def location(self):
        return self.generic_getter()

    @property
    def joint_positions(self):
        return self.generic_getter()

    @property
    def joint_count(self):
        return self.generic_getter()

    @property
    def tool_offset(self):
        return self.generic_getter()

    @tool_offset.setter
    def tool_offset(self, value):
        return self.generic_setter(value)

    @property
    def tool_mass(self):
        return self.generic_getter()

    @tool_mass.setter
    def tool_mass(self, value):
        return self.generic_setter(value)

    @property
    def gripper_position(self):
        return self.generic_getter()

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

class VirtualSerial(NiraapadClient):
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
    
    backend_type = utils.BACKENDS.SERIAL

    @staticmethod
    def list_devices(*args, **kwargs):
        return NiraapadClient.static_method(VirtualSerial.backend_type,
                                            *args, **kwargs)

    @staticmethod
    def list_device_ports(*args, **kwargs):
        return NiraapadClient.static_method(VirtualSerial.backend_type,
                                            *args, **kwargs)

    @classmethod
    def list_device_serials(cls, *args, **kwargs):
        return NiraapadClient.static_method(VirtualSerial.backend_type,
                                            *args, **kwargs)

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

    @property
    def info(self):
        return self.generic_getter()

    @property
    def serial_number(self):
        return self.generic_getter()

    @property
    def in_waiting(self):
        return self.generic_getter()

    @property
    def out_waiting(self):
        return self.generic_getter()

    @property
    def read_timeout(self):
        return self.generic_getter()

    @read_timeout.setter
    def read_timeout(self, value):
        self.generic_setter(value)

    @property
    def write_timeout(self):
        return self.generic_getter()

    @write_timeout.setter
    def write_timeout(self, value):
        self.generic_setter(value)

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
