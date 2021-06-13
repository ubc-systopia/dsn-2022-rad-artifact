import os
import sys
import grpc
import time
import pickle
import unittest
import argparse

from concurrent import futures

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

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc

from niraapad.shared.utils import *
from niraapad.shared.tracing import Tracer
from niraapad.middlebox.niraapad_server import NiraapadServer
from niraapad.lab_computer.ur3 import UR3Arm
from niraapad.lab_computer.ftdi_serial import Serial
from niraapad.lab_computer.niraapad_client import NiraapadClient

parser = argparse.ArgumentParser()
parser.add_argument('-D', '--distributed',
                    help='Distributed testing. Do not start server. Assume it is started on the provided host and port.',
                    action="store_true")
parser.add_argument('-H', '--host',
                    default='localhost',
                    help='Provide server hostname or IP address. Defaults to "ispy".',
                    type=str)
parser.add_argument('-P', '--port',
                    default='1337',
                    help='Provide the server port. Defaults to 1337.',
                    type=str)
parser.add_argument('-K', '--keysdir',
                    default= os.path.join(niraapad_path, "niraapad", "keys", "localhost"),
                    help='Provide path to the directory containing the "server.crt" file. Defaults to <project-dir>/niraapad/keys/.',
                    type=str)
parser.add_argument('-T', '--tracedir',
                    default= os.path.join(niraapad_path, "niraapad", "traces"),
                    help='Provide path to the trace directory. Defaults to <project-dir>/niraapad/traces/.',
                    type=str)
                    
args=parser.parse_args()

class TestN9Backend(unittest.TestCase):
    
    def setUp(self):
        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir, args.keysdir)
            self.niraapad_server.start()
        
        NiraapadClient.start_niraapad_client_helper(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_static_methods(self):
        for mo in MO:
            NiraapadClient.mo = mo
            serial_devices_info = Serial.list_devices()
            device_ports = Serial.list_device_ports()
            device_serials = Serial.list_device_serials()

    def test_init(self):
        """
        I have not implemented individual getter methods over RPC for each
        ttribute. So for now I will test each invocation manually by checking
        the output of a print statement on the server side. I will put in some
        assertions for the read_timeout and write_timeout properties, since
        getters for these are part of the API.
        By default, the print statement in DirectSerial.__init__ may be disabled
        or even missing (if we are using a pristine copy).
        """
        for mo in MO:
            NiraapadClient.mo = mo
            serial = Serial(connect=False)
            sys.stdout.flush()
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(baudrate=1, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(parity=2, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(stop_bits=3, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(data_bits=4, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(read_timeout=55, connect=False)
            self.assertEqual(55, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(write_timeout=66, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(66, serial.write_timeout)

            serial = Serial(connect_timeout=7, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(connect_retry=False, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(connect_settle_time=9, connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)

            serial = Serial(baudrate=11, parity=12, stop_bits=13, data_bits=14,
                            read_timeout=15, write_timeout=16, connect_timeout=17,
                            connect_retry=False, connect_settle_time=19,
                            connect=False)
            self.assertEqual(15, serial.read_timeout)
            self.assertEqual(16, serial.write_timeout)

            serial = Serial(baudrate=19, parity=18, stop_bits=17, data_bits=16,
                            read_timeout=15, write_timeout=14, connect_timeout=13,
                            connect_retry=False, connect_settle_time=11,
                            connect=False)
            self.assertEqual(15, serial.read_timeout)
            self.assertEqual(14, serial.write_timeout)

    def test_setters_and_getters(self):
        # TODO Try with a serial cable
        # Currently, self.device in ftdi_serial.py is None
        # Therefore, any method that invokes update_timeouts() fails
        for mo in MO:
            NiraapadClient.mo = mo
            serial = Serial(connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            # serial.read_timeout = 55
            # self.assertEqual(55, serial.read_timeout)
            # self.assertEqual(5, serial.write_timeout)
            # serial.write_timeout = 55
            # self.assertEqual(55, serial.read_timeout)
            # self.assertEqual(55, serial.write_timeout)
            # serial.read_timeout = 99
            # self.assertEqual(99, serial.read_timeout)
            # self.assertEqual(55, serial.write_timeout)
            # serial.write_timeout = 33
            # self.assertEqual(99, serial.read_timeout)
            # self.assertEqual(33, serial.write_timeout)


    def test_set_parameters(self):
        """
        Like test_init above, I will verify these call manually using print
        statements on the server side.
        """
        # TODO Try with a serial cable
        # Currently, self.device in ftdi_serial.py is None
        # Therefore, any method that invokes init_device() fails
        for mo in MO:
            NiraapadClient.mo = mo
            serial = Serial(connect=False)
            # serial.set_parameters(baudrate=10)
            # serial.set_parameters(parity=11)
            # serial.set_parameters(stop_bits=12)
            # serial.set_parameters(data_bits=13)
            # serial.set_parameters(baudrate=10, parity=11, stop_bits=12, data_bits=13)
            # serial.set_parameters(baudrate=14, parity=15, stop_bits=16, data_bits=17)
            # serial.set_parameters(baudrate=18, stop_bits=19)
            # serial.set_parameters(parity=20, data_bits=21)

    def test_tracing_1(self):
        for mo in MO:
            if mo == MO.DIRECT: continue
            NiraapadClient.mo = mo
            serial = Serial(connect=False)
        self.niraapad_server.stop_tracing()
        trace_file = self.niraapad_server.get_trace_file()
        backend_instance_id = 0
        for trace_msg_type, trace_msg in Tracer.parse_file(trace_file):
            backend_instance_id += 1
            self.assertEqual(trace_msg.req.backend_instance_id, backend_instance_id)
            self.assertEqual(pickle.loads(trace_msg.req.args), ())
            self.assertEqual(pickle.loads(trace_msg.req.kwargs), {'connect': False})
            self.assertEqual(trace_msg.resp, niraapad_pb2.InitializeResp(
                exception=pickle.dumps(None)))

    def test_tracing_2(self):
        NiraapadClient.mo = MO.VIA_MIDDLEBOX
        devices = Serial.list_devices() # 0
        device_ports = Serial.list_device_ports() # 1
        device_serials = Serial.list_device_serials() # 2
        serial = Serial(connect=False) # 3

        # TODO Try with a serial cable
        # Currently, self.device in ftdi_serial.py is None
        # Therefore, any method that invokes init_device() fails
        # serial.set_parameters() # 4
        # serial.set_parameters(stop_bits=3) # 5
        # serial.set_parameters(stop_bits=4, data_bits=4) # 6
        # serial.set_parameters(parity=5, stop_bits=5, data_bits=5) #7
        # serial.set_parameters(baudrate=6, parity=6, stop_bits=6, data_bits=6) # 8

        self.niraapad_server.stop_tracing()
        trace_file = self.niraapad_server.get_trace_file()
        counter = 0
        for trace_msg_type, trace_msg in Tracer.parse_file(trace_file):
            if counter == 0:
                self.assertEqual(trace_msg_type, "StaticMethodTraceMsg")
                self.assertEqual(trace_msg.req.method_name, "list_devices")
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
                self.assertEqual(len(pickle.loads(trace_msg.resp.resp)), len(devices))
            elif counter == 1:
                self.assertEqual(trace_msg_type, "StaticMethodTraceMsg")
                self.assertEqual(trace_msg.req.method_name, "list_device_ports")
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
                self.assertEqual(pickle.loads(trace_msg.resp.resp).sort(), device_ports.sort())
            elif counter == 2:
                self.assertEqual(trace_msg_type, "StaticMethodTraceMsg")
                self.assertEqual(trace_msg.req.method_name, "list_device_serials")
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
                self.assertEqual(pickle.loads(trace_msg.resp.resp).sort(), device_serials.sort())
            elif counter == 3:
                self.assertEqual(trace_msg_type, "InitializeTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {'connect': False})
                self.assertEqual(trace_msg.resp, niraapad_pb2.InitializeResp(
                    exception=pickle.dumps(None)))
            elif counter == 4:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
            elif counter == 5:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {'stop_bits': 3})
            elif counter == 6:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs),
                                 {'stop_bits': 4, 'data_bits': 4})
            elif counter == 7:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(
                    pickle.loads(trace_msg.req.kwargs),
                    {'parity': 5, 'stop_bits': 5, 'data_bits': 5})
            elif counter == 8:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(
                    pickle.loads(trace_msg.req.kwargs),
                    {'baudrate': 6, 'parity': 6, 'stop_bits': 6, 'data_bits': 6})
            else:
                self.fail("Shoudn't happen!")
            counter += 1

class TestUR3ArmBackend(unittest.TestCase):

    def setUp(self):
        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir, args.keysdir)
            self.niraapad_server.start()
        
        NiraapadClient.start_niraapad_client_helper(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server
    
    def test_init_vm(self):
        for mo in MO:    
            NiraapadClient.mo = mo
            ur3_arm = UR3Arm("192.168.236.128")
            
            jointpositions = [-54.36, -60.60, -85.60, -52.12, 121.92, 50.02]
            ur3_arm.move_joints(jointpositions)
            self.assertEqual([round(elem,2) for elem in ur3_arm.joint_positions], [round(elem,2) for elem in jointpositions])

            location = Location(x=50, y=-160, z=550, rx=-118.9, ry=56.53, rz=-135.8)
            ur3_arm.move_to_location(location)
            self.assertEqual(ur3_arm.location, location)

            self.assertEqual(ur3_arm.joint_count, 6)

            time.sleep(2)

    def test_init(self):
        for mo in MO:
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


def suite_n9():
    suite = unittest.TestSuite()
    suite.addTest(TestN9Backend('test_static_methods'))
    suite.addTest(TestN9Backend('test_init'))
    suite.addTest(TestN9Backend('test_setters_and_getters'))
    suite.addTest(TestN9Backend('test_set_parameters'))
    suite.addTest(TestN9Backend('test_tracing_1'))
    suite.addTest(TestN9Backend('test_tracing_2'))
    return suite

def suite_ur3arm():
    suite = unittest.TestSuite()
    #suite.addTest(TestUR3ArmBackend('test_init_vm'))
    suite.addTest(TestUR3ArmBackend('test_init'))
    suite.addTest(TestUR3ArmBackend('test_exception_handling'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite_n9())
    runner.run(suite_ur3arm())
