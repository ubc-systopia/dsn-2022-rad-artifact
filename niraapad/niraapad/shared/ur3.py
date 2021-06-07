from typing import Optional, List, Union
import time
import math
import urx
from urx import ursecmon
import math3d
from hein_robots.robotics import Location, Twist, Wrench, Units, Frame
from hein_robots.robotiq.gripper import RobotiqGripper
from niraapad.shared import robot_arms

class DirectUR3Arm(robot_arms.DirectRobotArm):
    def __init__(self, host: str = '192.168.0.100', default_velocity: float = 250, max_velocity: float = 500, position_units: str = Units.MILLIMETERS,
                 default_joint_velocity: float = 20.0, max_joint_velocity = 180.0, gripper_default_velocity: float = 0.5, gripper_default_force: float = 0.5,
                 gripper_id: int = 1, connect: bool = True):
        super().__init__(default_velocity=default_velocity, max_velocity=max_velocity, position_units=position_units,
                         gripper_default_velocity=gripper_default_velocity, gripper_default_force=gripper_default_force)
        self._default_joint_velocity = default_joint_velocity
        self.max_joint_velocity = max_joint_velocity
        self.host = host
        self._robot: Optional[urx.Robot] = None
        self.gripper = RobotiqGripper(self.host, id=gripper_id, connect=False)

        if connect:
            self.connect()

    @property
    def robot(self) -> urx.Robot:
        if self._robot is None:
            raise robot_arms.RobotArmNotConnectedError(f'UR3 arm not connected, try running connect()')

        return self._robot

    @property
    def connected(self) -> bool:
        return self._robot is not None

    @property
    def default_joint_velocity(self) -> float:
        return self._default_velocity

    @default_joint_velocity.setter
    def default_joint_velocity(self, value: float):
        if value < 0 or value > self.max_joint_velocity:
            raise robot_arms.RobotArmInvalidVelocityError(f'Invalid velocity: {value} degrees/s, must be less than {self.max_joint_velocity} degrees/s')

        self._default_velocity = value

    @property
    def acceleration(self) -> float:
        return 0.0

    @property
    def velocity(self) -> float:
        return 0.0

    @property
    def pose(self):
        return self.robot.get_pose()

    @property
    def location(self) -> Location:
        return Location.from_matrix(self.pose.array).convert_m_to_mm()

    @property
    def joint_positions(self) -> List[float]:
        return [math.degrees(position) for position in self.robot.getj()]

    @property
    def joint_count(self) -> int:
        return len(self.joint_positions)

    @property
    def tool_offset(self) -> Location:
        raise robot_arms.RobotArmNotSupportedError(f'Reading UR3Arm tool_offset not supported')

    @tool_offset.setter
    def tool_offset(self, value: Location):
        self.robot.set_tcp(*value.position, *value.orientation)

    @property
    def tool_mass(self) -> float:
        raise robot_arms.RobotArmNotSupportedError(f'Reading UR3Arm tool_mass not supported')

    @tool_mass.setter
    def tool_mass(self, value: float):
        self.robot.set_payload(value)

    @property
    def gripper_position(self) -> float:
        return self.gripper.position

    def connect(self, retries=5):
        while retries > 0:
            try:
                self._robot = urx.Robot(self.host)
                self.gripper.connect()
                return
            except ursecmon.TimeoutException:
                print('Retrying')
                time.sleep(1)
                retries -= 1

        raise robot_arms.RobotArmConnectionError(f'Cannot connect to UR3 at host {self.host}')

    def disconnect(self):
        self._robot.close()
        self._robot = None
        self.gripper.disconnect()

    def stop(self):
        self.robot.stop()

    def close(self):
        self.robot.close()

    def emergency_stop(self):
        self.stop()

    def wait(self, timeout: Optional[float] = None, wait_for_running: bool = False):
        start_time = time.time()

        if wait_for_running:
            while not self.robot.is_program_running():
                if timeout is not None and (time.time() - start_time) > timeout:
                    raise robot_arms.RobotArmWaitTimeoutError(f'Timeout while waiting for UR3 arm to start')

                time.sleep(0.01)

        while self.robot.is_program_running():
            if timeout is not None and (time.time() - start_time) > timeout:
                raise robot_arms.RobotArmWaitTimeoutError(f'Timeout while waiting for UR3 arm to stop')

            time.sleep(0.01)

    def move_to_location(self, location: Location, frame: Optional[Frame] = None,
                         velocity: Optional[float] = None, acceleration: Optional[float] = None,
                         relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        vel = velocity if velocity is not None else self._default_velocity
        acc = acceleration if acceleration is not None else vel * 2
        # use the reference frame (or an identity frame) to transform the relative location to a location in the base reference frame
        relative_position = (frame or Location()) * location
        transform = self.robot.csys * math3d.Transform(relative_position.convert_mm_to_m().matrix)
        distance = self.robot._get_lin_dist(transform.pose_vector)

        self.robot.movel(transform.pose_vector, acc=acc / 1000, vel=vel / 1000, relative=relative, wait=False)

        # don't wait if we aren't going to move
        if wait and distance > 1e-3:
            self.wait(timeout, wait_for_running=True)

    def move_joints(self, joint_positions: List[float],
                    velocity: Optional[float] = None, acceleration: Optional[float] = None,
                    relative: bool = False, wait: bool = True, timeout: Optional[float] = None):
        if len(joint_positions) != self.joint_count:
            raise robot_arms.RobotArmInvalidJointsError(f'Invalid number of UR3 arm joints, must be {self.joint_count}')

        vel = velocity if velocity is not None else self._default_joint_velocity
        acc = acceleration if acceleration is not None else vel * 2
        joint_radians = [math.radians(position) for position in joint_positions]
        distance = self.robot._get_joints_dist(joint_radians)

        try:
            self.robot.movej(joint_radians, vel=math.radians(vel), acc=math.radians(acc), relative=relative, wait=False)
        except urx.urrobot.RobotException:
            pass

        # don't wait if we aren't going to move
        if wait and distance > 1e-3:
            self.wait(timeout, wait_for_running=True)

    def move_circular(self, midpoint: Location, end: Location, frame: Optional[Frame] = None,
                      velocity: Optional[float] = None, acceleration: Optional[float] = None,
                      wait: bool = True, timeout: Optional[float] = None):
        vel = velocity if velocity is not None else self._default_velocity
        acc = acceleration if acceleration is not None else vel * 2
        # use the reference frame (or an identity frame) to transform the relative location to a location in the base reference frame
        relative_midpoint = (frame or Location()) * midpoint
        relative_end = (frame or Location()) * end
        transform_midpoint = self.robot.csys * math3d.Transform(relative_midpoint.convert_mm_to_m().matrix)
        transform_end = self.robot.csys * math3d.Transform(relative_end.convert_mm_to_m().matrix)

        self.robot.movec(transform_midpoint.pose_vector, transform_end.pose_vector, acc=acc / 1000, vel=vel / 1000, wait=False)

        if wait:
            self.wait(timeout, wait_for_running=True)

    def wait_for_gripper_stop(self, timeout: Optional[float] = None):
        self.gripper.wait_for_stop(timeout=timeout)

    def open_gripper(self, position: Optional[Union[float, bool]] = None, force: Optional[float] = None, velocity: Optional[float] = None,
                     wait: bool = True, timeout: Optional[float] = None):
        if position is None:
            position = 0.0
        elif isinstance(position, bool):
            position = 0.0 if position else 1.0

        self.gripper.move(position, force=force or self.gripper_default_force, velocity=velocity or self.gripper_default_velocity, wait=wait, timeout=timeout or 10.0)

################################################################################
################################################################################
########################## MAIN MODIFICATIONS START HERE #######################
################################################################################
################################################################################

import inspect

import niraapad.shared.utils as utils

from niraapad.shared.robot_arms import RobotArm
#from niraapad.lab_computer.niraapad_client import NiraapadClient

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

    backend_type = utils.BACKEND_UR3_ARM

    @staticmethod
    def get_func_arg_names(method_name):
        return eval("inspect.getfullargspec(%s.%s).args" % \
            (UR3Arm.backend_type, method_name))

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
