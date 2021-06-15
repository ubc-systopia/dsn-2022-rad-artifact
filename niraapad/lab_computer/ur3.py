import inspect

from hein_robots.universal_robots.ur3 import UR3Arm as DirectUR3Arm

import niraapad.shared.utils as utils

from niraapad.lab_computer.niraapad_client import NiraapadClient

class RobotArm(NiraapadClient):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    RobotArm", which is renamed to "class DirectRobotArm" (see above). In addition,
    the class maintains three operation modes as summarized above along in
    "class MO". In order to do so, this class simply forwards
    each function call to the respective function call in the respective
    DirectRobotArm class object (class objects are not involved in the case of
    static functions), or to the respective function call in the global object
    of type "class NiraapadClientHelper" (which in turn invokes an RPC to the
    middlebox), or both.
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

class UR3Arm(RobotArm):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    UR3Arm", which is renamed to "class DirectUR3Arm" (see above). In addition,
    the class maintains three operation modes as summarized above along in
    "class MO". In order to do so, this class simply forwards
    each function call to the respective function call in the respective
    DirectUR3Arm class object (class objects are not involved in the case of
    static functions), or to the respective function call in the global object
    of type "class NiraapadClientHelper" (which in turn invokes an RPC to the
    middlebox), or both.
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
