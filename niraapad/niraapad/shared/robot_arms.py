from typing import Optional, List, Union
from hein_robots.robotics import Location, Twist, Wrench, Cartesian, Orientation, Units, Frame
from hein_robots.base.actuators import Actuator
from hein_robots.base.grippers import Gripper


class DirectRobotArm:
    def __init__(self, default_velocity: float = 250, max_velocity: float = 500, position_units: str = Units.MILLIMETERS,
                 gripper_default_velocity: float = 0.5, gripper_default_force: float = 0.5):
        self._position_units = position_units
        self._default_velocity = default_velocity
        self._max_velocity = max_velocity
        self._gripper_default_velocity = gripper_default_velocity
        self._gripper_default_force = gripper_default_force

    @property
    def connected(self) -> bool:
        return False

    @property
    def max_velocity(self) -> float:
        return self._max_velocity

    @max_velocity.setter
    def max_velocity(self, value: float):
        self._max_velocity = value

    @property
    def default_velocity(self) -> float:
        return self._default_velocity

    @default_velocity.setter
    def default_velocity(self, value: float):
        if value < 0 or value > self.max_velocity:
            raise RobotArmInvalidVelocityError(f'Invalid velocity: {value} m/s, must be less than {self.max_velocity} m/s')

        self._default_velocity = value

    @property
    def acceleration(self) -> float:
        print("Finding acceleration")
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} acceleration not supported')

    @property
    def velocity(self) -> float:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} velocity not supported')

    @property
    def location(self) -> Location:
        return Location()

    @property
    def twist(self) -> Twist:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} twist not supported')

    @property
    def wrench(self) -> Wrench:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} wrench not supported')

    @property
    def joint_positions(self) -> List[float]:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} joint_positions not supported')

    @property
    def joint_count(self) -> int:
        return len(self.joint_positions)

    @property
    def gripper_position(self) -> float:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} gripper_position not supported')

    @property
    def gripper_velocity(self) -> float:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} gripper_velocity not supported')

    @property
    def gripper_default_velocity(self) -> float:
        return self._gripper_default_velocity

    @gripper_default_velocity.setter
    def gripper_default_velocity(self, velocity: float):
        if velocity < 0 or velocity > 1:
            raise RobotArmGripperInvalidVelocityError(f'Invalid velocity, must be float between 0 and 1: {velocity}')

        self._gripper_default_velocity = velocity

    @property
    def gripper_default_force(self) -> float:
        return self._gripper_default_velocity

    @gripper_default_force.setter
    def gripper_default_force(self, force: float):
        if force < 0 or force > 1:
            raise RobotArmGripperInvalidForceError(f'Invalid force, must be float between 0 and 1: {force}')

        self._gripper_default_force = force

    @property
    def tool_offset(self) -> Location:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} tool_offset not supported')

    @tool_offset.setter
    def tool_offset(self, value: Location):
        raise RobotArmNotSupportedError(f'Setting {self.__class__.__name__} tool_offset not supported')

    @property
    def tool_mass(self) -> float:
        raise RobotArmNotSupportedError(f'Reading {self.__class__.__name__} tool_mass not supported')

    @tool_mass.setter
    def tool_mass(self, value: float):
        raise RobotArmNotSupportedError(f'Setting {self.__class__.__name__} tool_mass not supported')

    def connect(self):
        pass

    def disconnect(self):
        pass

    def stop(self):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} stop not supported')

    def pause(self):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} pause not supported')

    def resume(self):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} resume not supported')

    def emergency_stop(self):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} emergency_stop not supported')

    def clear_faults(self):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} clear_faults not supported')

    def home(self, wait: bool = True):
        pass

    def move(self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None,
             rx: Optional[float] = None, ry: Optional[float] = None, rz: Optional[float] = None,
             frame: Optional[Frame] = None, velocity: Optional[float] = None, acceleration: Optional[float] = None,
             relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        if not relative:
            location = Location(
                x=self.location.position.x if x is None else x,
                y=self.location.position.y if y is None else y,
                z=self.location.position.z if z is None else z,
                ry=self.location.orientation.ry if ry is None else ry,
                rx=self.location.orientation.rx if rx is None else rx,
                rz=self.location.orientation.rz if rz is None else rz,
            )
        else:
            location = Location(x or 0, y or 0, z or 0, rx or 0, ry or 0, rz or 0)

        self.move_to_location(location, frame=frame, velocity=velocity, acceleration=acceleration, relative=relative, wait=wait,
                              timeout=timeout)

    def move_tool(self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None,
             rx: Optional[float] = None, ry: Optional[float] = None, rz: Optional[float] = None,
             velocity: Optional[float] = None, acceleration: Optional[float] = None,
             wait: bool = True, timeout: Optional[float] = None):
        location = Location(x or 0, y or 0, z or 0, rx or 0, ry or 0, rz or 0)
        self.move_to_location(location, frame=self.location, velocity=velocity, acceleration=acceleration, relative=False, wait=wait,
                              timeout=timeout)

    def move_to_location(self, location: Location, frame: Optional[Frame] = None,
                         velocity: Optional[float] = None, acceleration: Optional[float] = None,
                         relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_tool_to_location(self, location: Location,
                         velocity: Optional[float] = None, acceleration: Optional[float] = None,
                         relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        self.move_to_location(location, frame=self.location,
                              velocity=velocity, acceleration=acceleration,
                              relative=relative, wait=wait, timeout=timeout)

    def move_to_locations(self, *locations: Location, frame: Optional[Frame] = None,
                          velocity: Optional[float] = None, acceleration: Optional[float] = None,
                          relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        for location in locations:
            self.move_to_location(location, frame=frame,
                                  velocity=velocity, acceleration=acceleration,
                                  relative=relative, wait=wait, timeout=timeout)

    def move_tool_to_locations(self, *locations: Location,
                          velocity: Optional[float] = None, acceleration: Optional[float] = None,
                          relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        self.move_to_locations(*locations, velocity=velocity, acceleration=acceleration,
                               relative=relative, wait=wait, timeout=timeout)

    def move_joints(self, joint_positions: List[float],
                    velocity: Optional[float] = None, acceleration: Optional[float] = None,
                    relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        pass

    def move_joint(self, joint_id: int, position: float,
                   velocity: Optional[float] = None, acceleration: Optional[float] = None,
                   relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        positions = list(self.joint_positions)
        positions[joint_id] = positions[joint_id] + position if relative else position

        self.move_joints(positions, velocity=velocity, acceleration=acceleration, relative=relative, wait=wait, timeout=timeout)

    def move_twist(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, rx: float = 0.0, ry: float = 0.0, rz: float = 0.0,
                   duration: Optional[float] = None, wait: bool = True, timeout: Optional[float] = None):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} move_twist not supported')

    def move_twist_to(self, twist: Twist, duration: Optional[float] = None, wait: bool = True, timeout: Optional[float] = None):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} move_twist_to stop not supported')

    def wait(self, timeout: Optional[float] = None):
        pass

    def wait_for_gripper_stop(self, timeout: Optional[float] = None):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} gripper not supported')

    def open_gripper(self, position: Optional[Union[float, bool]] = None, wait: bool = True, timeout: Optional[float] = None):
        raise RobotArmNotSupportedError(f'{self.__class__.__name__} gripper not supported')

    def close_gripper(self, position: Optional[Union[float, bool]] = None, wait: bool = True, timeout: Optional[float] = None):
        if position is None:
            position = False
        elif isinstance(position, bool):
            position = not position

        self.open_gripper(position, wait=wait, timeout=timeout)


class RobotArmError(Exception):
    pass


class RobotArmNotConnectedError(RobotArmError):
    pass


class RobotArmConnectionError(RobotArmError):
    pass


class RobotArmNotSupportedError(RobotArmError):
    pass


class RobotArmUnitsError(RobotArmError):
    pass


class RobotArmMovementError(RobotArmError):
    pass


class RobotArmInvalidJointsError(RobotArmError):
    pass


class RobotArmInvalidVelocityError(RobotArmError):
    pass


class RobotArmWaitTimeoutError(RobotArmError):
    pass


class RobotArmGripperTimeoutError(RobotArmError):
    pass


class RobotArmGripperInvalidForceError(RobotArmError):
    pass


class RobotArmGripperInvalidVelocityError(RobotArmError):
    pass

################################################################################
################################################################################
########################## MAIN MODIFICATIONS START HERE #######################
################################################################################
################################################################################

import inspect

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

    backend_type = utils.BACKEND_ROBOT_ARM

    @staticmethod
    def get_func_arg_names(method_name):
        return eval("inspect.getfullargspec(%s.%s).args" % \
            (RobotArm.backend_type, method_name))

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
