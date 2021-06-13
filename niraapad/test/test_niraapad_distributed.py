import os
import sys
import unittest
import argparse

# Path to this file test_niraapad.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))
sys.path.append(niraapad_path)

# Path to the hein_robots git repo (submodule)
hein_robots_path = os.path.join(niraapad_path, "hein_robots")
sys.path.append(hein_robots_path)

# Path to the urx git repo (submodule)
urx_path = os.path.join(niraapad_path, "python-urx")
sys.path.append(urx_path)

# Path to the ftdi_serial git repo (submodule)
ftdi_serial_path = os.path.join(niraapad_path, "ftdi_serial")
sys.path.append(ftdi_serial_path)

from hein_robots.robotics import Units
from hein_robots.base import robot_arms

from niraapad.shared.utils import *
from niraapad.lab_computer.ur3 import UR3Arm
from niraapad.lab_computer.ftdi_serial import Serial
from niraapad.lab_computer.niraapad_client import NiraapadClient

parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host',
                    default='ispy',
                    help='Provide server hostname or IP address. Defaults to "ispy".',
                    type=str)
parser.add_argument('-P', '--port',
                    default='1337',
                    help='Provide the server port. Defaults to 1337.',
                    type=str)
parser.add_argument('-K', '--keysdir',
                    default= os.path.join(niraapad_path, "niraapad", "keys"),
                    help='Provide path to the directory containing the "server.crt" file. Defaults to <project-dir>/niraapad/keys/.',
                    type=str)
args=parser.parse_args()

class TestUR3ArmBackendDistributed(unittest.TestCase):

    def setUp(self):
        #print("Starting NiraapadClientHelper") 
        NiraapadClient.start_niraapad_client_helper(args.host, args.port, args.keysdir)
        NiraapadClient.mo = MO.VIA_MIDDLEBOX


    def tearDown(self):
        pass

    def test_simple_init(self):
        for mo in MO:
            if mo == MO.DIRECT: continue
            NiraapadClient.mo = mo
            #print("Initializing UR3Arm")
            ur3_arm = UR3Arm(connect=False)
    
    def test_init(self):
        for mo in MO:
            if mo == MO.DIRECT: continue
            NiraapadClient.mo = mo
            ur3_arm = UR3Arm(connect=False)
            self.assertEqual(ur3_arm.default_velocity, 250)
            self.assertEqual(ur3_arm.max_velocity, 500)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', connect=False)
            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 500)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, position_units=Units.METERS, connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, position_units=Units.METERS,
                default_joint_velocity=3, connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, position_units=Units.METERS,
                default_joint_velocity=3, max_joint_velocity=4, connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, position_units=Units.METERS,
                default_joint_velocity=3, max_joint_velocity=4,
                gripper_default_velocity=5, connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, position_units=Units.METERS,
                default_joint_velocity=3, max_joint_velocity=4,
                gripper_default_velocity=5, gripper_default_force=6,
                connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', default_velocity=1,
                max_velocity=2, position_units=Units.METERS,
                default_joint_velocity=3, max_joint_velocity=4,
                gripper_default_velocity=5, gripper_default_force=6,
                gripper_id=7, connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(connect=False, gripper_id=1,
                gripper_default_force=0.2, gripper_default_velocity=0.3,
                max_joint_velocity=0.4, default_joint_velocity=0.5,
                position_units=Units.RADIANS, max_velocity=0.6,
                default_velocity=0.7, host='1.2.3.4')
            self.assertEqual(ur3_arm.default_velocity, 0.7)
            self.assertEqual(ur3_arm.max_velocity, 0.6)
            self.assertEqual(ur3_arm.default_joint_velocity, ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.3)
            self.assertEqual(ur3_arm.connected, False)
    
    def test_exception_handling(self):
        for mo in MO:
            if mo == MO.DIRECT: continue
            NiraapadClient.mo = mo
            ur3_arm = UR3Arm(max_joint_velocity=100.0, connect=False)
            with self.assertRaises(robot_arms.RobotArmNotConnectedError):
                robot = ur3_arm.robot
            with self.assertRaises(robot_arms.RobotArmInvalidVelocityError):
                ur3_arm.default_joint_velocity = -1.0
            with self.assertRaises(robot_arms.RobotArmInvalidVelocityError):
                ur3_arm.default_joint_velocity = 101.0
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                tool_offset = ur3_arm.tool_offset
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                tool_mass = ur3_arm.tool_mass
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                twist = ur3_arm.twist
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                wrench = ur3_arm.wrench
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                ur3_arm.pause()
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                ur3_arm.resume()
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                ur3_arm.clear_faults()
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                ur3_arm.move_twist()
            with self.assertRaises(robot_arms.RobotArmNotSupportedError):
                ur3_arm.move_twist_to(twist=None)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUR3ArmBackendDistributed('test_simple_init'))
    suite.addTest(TestUR3ArmBackendDistributed('test_init'))
    suite.addTest(TestUR3ArmBackendDistributed('test_exception_handling'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())