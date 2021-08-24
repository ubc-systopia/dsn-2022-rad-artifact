import os
import sys
import grpc
import time
import types
import pickle
import unittest
import argparse

from typing import Optional
from concurrent import futures

from ika.magnetic_stirrer import MagneticStirrer

# Path to this file test_niraapad.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))

# This import is needed if we are not testing using the PyPI (or TestPyPI)
# niraapad package but instead using the niraapad files from source
sys.path.append(niraapad_path)

# ===== THESE ARE IMPORTANT FOR MONKEY PATCHING =====
import niraapad.backends

# Ignoring class ftdi_serial.Serial because we have
# decided to virtualize the Device classes instead,
# which actually are closer to the network layer
# from niraapad.backends import DirectSerial, VirtualSerial

# # Among all the Device subclasses,
# # supporting classes FtdiDevice and PySerialDevice,
# # but ignoring class ftdi_serial.MockDevice,
# # because it is not supported in ftdi-serial v0.1.9
# from niraapad.backends import DirectMockDevice
from niraapad.backends import DirectFtdiDevice
from niraapad.backends import DirectPySerialDevice
# from niraapad.backends import DirectC9SerialDevice

# The UR3Arm does not directly rely on the Device
# classes (i.e., serial communication) but instead
# communicates with the lab computer over LAN
from niraapad.backends import DirectUR3Arm
# ===================================================

from ftdi_serial import Serial, SerialReadTimeoutException
from ftdi_serial import Device, FtdiDevice, PySerialDevice  #, MockDevice
from hein_robots.universal_robots.ur3 import UR3Arm
from hein_robots.robotics import Location, Units
from hein_robots.base import robot_arms
from north_c9.controller import C9Controller
from north_c9.serial import C9SerialDevice
from north_robots.n9 import N9Robot
from mtbalance import ArduinoAugmentedQuantos
from north_devices.pumps.tecan_cavro import TecanCavro

import serial as PySerialDriver

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc

from niraapad.shared.utils import *
from niraapad.shared.tracing import Tracer
from niraapad.middlebox.niraapad_server import NiraapadServer
from niraapad.lab_computer.niraapad_client import NiraapadClient


class MyC9ControllerWithEmptyPing(C9Controller):

    def __init__(self, device_serial: str, connect: bool,
                 use_joystick: bool) -> None:
        super().__init__(device_serial=device_serial,
                         connect=connect,
                         use_joystick=use_joystick)

    def ping(elf, timeout: float = 1.0, retries: int = 5):
        pass


class MyC9ControllerWithNewDisconnect(C9Controller):

    def __init__(self, device_serial: str, connect: bool,
                 use_joystick: bool) -> None:
        super().__init__(device_serial=device_serial,
                         connect=connect,
                         use_joystick=use_joystick)

    def disconnect(self):
        self.connection.disconnect()
        if hasattr(self, "joystick"):
            if self.joystick.running:
                self.joystick.stop()


class MyC9Controller(MyC9ControllerWithEmptyPing,
                     MyC9ControllerWithNewDisconnect):

    def __init__(self, device_serial: str, connect: bool,
                 use_joystick: bool) -> None:
        super().__init__(device_serial=device_serial,
                         connect=connect,
                         use_joystick=use_joystick)


parser = argparse.ArgumentParser()
parser.add_argument(
    '-D',
    '--distributed',
    help=
    'Distributed testing. Do not start server. Assume it is started on the provided host and port.',
    action="store_true")
parser.add_argument(
    '-H',
    '--host',
    default='localhost',
    help='Provide server hostname or IP address. Defaults to "localhost".',
    type=str)
parser.add_argument('-P',
                    '--port',
                    default='1337',
                    help='Provide the server port. Defaults to 1337.',
                    type=str)
parser.add_argument(
    '-K',
    '--keysdir',
    default=os.path.join(niraapad_path, "niraapad", "keys", "localhost"),
    help=
    'Provide path to the directory containing the "server.crt" file. Defaults to <project-dir>/niraapad/keys/localhost.',
    type=str)
parser.add_argument(
    '-T',
    '--tracedir',
    default=os.path.join(niraapad_path, "niraapad", "traces"),
    help=
    'Provide path to the trace directory. Defaults to <project-dir>/niraapad/traces/.',
    type=str)
parser.add_argument('-S',
                    '--secure',
                    help='Use a secure connection.',
                    action="store_true")

args = parser.parse_args()


class TestC9Controller(unittest.TestCase):

    def setUp(self):
        if args.secure == False:
            args.keysdir = None

        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir,
                                                  args.keysdir)
            self.niraapad_server.start()

        NiraapadClient.connect_to_middlebox(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_instance_type(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
            device_serial = 'AB0KPC1S'
            c9 = C9Controller(device_serial=device_serial,
                              use_joystick=False,
                              connect=False)
            if mo == MO.DIRECT:
                self.assertIsInstance(c9.connection, Serial)
            elif mo == MO.DIRECT_PLUS_MIDDLEBOX:
                self.assertIsInstance(c9.connection, Serial)
            elif mo == MO.VIA_MIDDLEBOX:
                self.assertIsInstance(c9.connection, Serial)
            else:
                self.assertFalse(True)

    def test_device_methods(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo

            device_serial = 'AB0KPC1S'
            c9 = C9Controller(device_serial=device_serial,
                              use_joystick=False,
                              connect=False)

            self.assertEqual(c9.connection.device, None)
            c9.connection.open_device()
            self.assertNotEqual(c9.connection.device, None)

            c9.connection.device.clear()
            c9.connection.device.reset()
            c9.connection.device.set_baud_rate(115200)
            c9.connection.device.set_parameters(Serial.DATA_BITS_8,
                                                Serial.STOP_BITS_1,
                                                Serial.PARITY_NONE)

            read_timeouts_ms = [1, 10, 100, 1000, 2000]
            for read_timeout_ms in read_timeouts_ms:
                c9.connection.device.set_timeouts(read_timeout_ms, 0)
                start = time.time()
                c9.connection.device.read(1)
                end = time.time()
                self.assertGreater(end - start, read_timeout_ms / 1000.0)

            c9.connection.device.close()

    def test_connection_methods(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo

            device_serial = 'AB0KPC1S'

            c9 = MyC9Controller(device_serial=device_serial,
                                use_joystick=False,
                                connect=True)

            read_timeouts_ms = [1, 10, 100, 1000, 2000]
            for read_timeout_ms in read_timeouts_ms:
                c9.connection.read_timeout = read_timeout_ms / 1000.0
                start = time.time()
                with self.assertRaises(SerialReadTimeoutException):
                    c9.connection.read(1)
                end = time.time()
                self.assertGreater(end - start, read_timeout_ms / 1000.0)

            c9.disconnect()

    def test_py_serial_device(self):
        for mo in MO:
            self.assertEqual(PySerialDevice.PARITIES[0],
                             PySerialDriver.PARITY_NONE)
            self.assertEqual(PySerialDevice.PARITIES[1],
                             PySerialDriver.PARITY_ODD)
            self.assertEqual(PySerialDevice.PARITIES[2],
                             PySerialDriver.PARITY_EVEN)
            self.assertEqual(PySerialDevice.STOP_BITS[0],
                             PySerialDriver.STOPBITS_ONE)
            self.assertEqual(PySerialDevice.STOP_BITS[2],
                             PySerialDriver.STOPBITS_TWO)


class TestN9Backend(unittest.TestCase):

    def setUp(self):
        if args.secure == False:
            args.keysdir = None

        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir,
                                                  args.keysdir)
            self.niraapad_server.start()

        NiraapadClient.connect_to_middlebox(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_class_variables(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo

            #         self.assertEqual(Serial.FT_OK, DirectSerial.FT_OK)
            #         self.assertEqual(Serial.FT_PURGE_RX, DirectSerial.FT_PURGE_RX)
            #         self.assertEqual(Serial.FT_PURGE_TX, DirectSerial.FT_PURGE_TX)
            #         self.assertEqual(Serial.PARITY_NONE, DirectSerial.PARITY_NONE)
            #         self.assertEqual(Serial.PARITY_ODD, DirectSerial.PARITY_ODD)
            #         self.assertEqual(Serial.PARITY_EVEN, DirectSerial.PARITY_EVEN)
            #         self.assertEqual(Serial.STOP_BITS_1, DirectSerial.STOP_BITS_1)
            #         self.assertEqual(Serial.STOP_BITS_2, DirectSerial.STOP_BITS_2)
            #         self.assertEqual(Serial.DATA_BITS_7, DirectSerial.DATA_BITS_7)
            #         self.assertEqual(Serial.DATA_BITS_8, DirectSerial.DATA_BITS_8)

            self.assertEqual(Serial.FT_OK, 0)
            self.assertEqual(Serial.FT_PURGE_RX, 1)
            self.assertEqual(Serial.FT_PURGE_TX, 2)
            self.assertEqual(Serial.PARITY_NONE, 0)
            self.assertEqual(Serial.PARITY_ODD, 1)
            self.assertEqual(Serial.PARITY_EVEN, 2)
            self.assertEqual(Serial.STOP_BITS_1, 0)
            self.assertEqual(Serial.STOP_BITS_2, 2)
            self.assertEqual(Serial.DATA_BITS_7, 7)
            self.assertEqual(Serial.DATA_BITS_8, 8)

    #         Serial.FT_OK += 1
    #         Serial.FT_PURGE_RX += 1
    #         Serial.FT_PURGE_TX += 1
    #         Serial.PARITY_NONE += 1
    #         Serial.PARITY_ODD += 1
    #         Serial.PARITY_EVEN += 1
    #         Serial.STOP_BITS_1 += 1
    #         Serial.STOP_BITS_2 += 1
    #         Serial.DATA_BITS_7 += 1
    #         Serial.DATA_BITS_8 += 1

    #         self.assertEqual(Serial.FT_OK, 1)
    #         self.assertEqual(Serial.FT_PURGE_RX, 2)
    #         self.assertEqual(Serial.FT_PURGE_TX, 3)
    #         self.assertEqual(Serial.PARITY_NONE, 1)
    #         self.assertEqual(Serial.PARITY_ODD, 2)
    #         self.assertEqual(Serial.PARITY_EVEN, 3)
    #         self.assertEqual(Serial.STOP_BITS_1, 1)
    #         self.assertEqual(Serial.STOP_BITS_2, 3)
    #         self.assertEqual(Serial.DATA_BITS_7, 8)
    #         self.assertEqual(Serial.DATA_BITS_8, 9)

    #         Serial.FT_OK -= 1
    #         Serial.FT_PURGE_RX -= 1
    #         Serial.FT_PURGE_TX -= 1
    #         Serial.PARITY_NONE -= 1
    #         Serial.PARITY_ODD -= 1
    #         Serial.PARITY_EVEN -= 1
    #         Serial.STOP_BITS_1 -= 1
    #         Serial.STOP_BITS_2 -= 1
    #         Serial.DATA_BITS_7 -= 1
    #         Serial.DATA_BITS_8 -= 1

    def test_static_methods(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
            serial_devices_info = Serial.list_devices()
            device_ports = Serial.list_device_ports()
            device_serials = Serial.list_device_serials()

    def test_init(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
            serial = Serial(connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(baudrate=1, connect=False)
            self.assertEqual(1, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(parity=2, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(2, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(stop_bits=3, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(3, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(data_bits=4, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(4, serial.data_bits)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(read_timeout=55, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(55, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(write_timeout=66, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(66, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(connect_timeout=7, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(7, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(connect_retry=False, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(False, serial.connect_retry)
            self.assertEqual(3, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(connect_settle_time=9, connect=False)
            self.assertEqual(115200, serial.baudrate)
            self.assertEqual(Serial.PARITY_NONE, serial.parity)
            self.assertEqual(Serial.STOP_BITS_1, serial.stop_bits)
            self.assertEqual(Serial.DATA_BITS_8, serial.data_bits)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            self.assertEqual(30, serial.connect_timeout)
            self.assertEqual(True, serial.connect_retry)
            self.assertEqual(9, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(baudrate=11,
                            parity=12,
                            stop_bits=13,
                            data_bits=14,
                            read_timeout=15,
                            write_timeout=16,
                            connect_timeout=17,
                            connect_retry=False,
                            connect_settle_time=19,
                            connect=False)
            self.assertEqual(11, serial.baudrate)
            self.assertEqual(12, serial.parity)
            self.assertEqual(13, serial.stop_bits)
            self.assertEqual(14, serial.data_bits)
            self.assertEqual(15, serial.read_timeout)
            self.assertEqual(16, serial.write_timeout)
            self.assertEqual(17, serial.connect_timeout)
            self.assertEqual(False, serial.connect_retry)
            self.assertEqual(19, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

            serial = Serial(baudrate=19,
                            parity=18,
                            stop_bits=17,
                            data_bits=16,
                            read_timeout=15,
                            write_timeout=14,
                            connect_timeout=13,
                            connect_retry=False,
                            connect_settle_time=11,
                            connect=False)
            self.assertEqual(19, serial.baudrate)
            self.assertEqual(18, serial.parity)
            self.assertEqual(17, serial.stop_bits)
            self.assertEqual(16, serial.data_bits)
            self.assertEqual(15, serial.read_timeout)
            self.assertEqual(14, serial.write_timeout)
            self.assertEqual(13, serial.connect_timeout)
            self.assertEqual(False, serial.connect_retry)
            self.assertEqual(11, serial.connect_settle_time)
            self.assertEqual(b'', serial.input_buffer)
            self.assertEqual(b'', serial.output_buffer)
            self.assertEqual(False, serial.connected)

    def test_setters_and_getters(self):
        # TODO Try with a serial cable
        # Currently, self.device in ftdi_serial.py is None
        # Therefore, any method that invokes update_timeouts() fails
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
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
            NiraapadClient.niraapad_mo = mo
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
        # TODO Ideally, in the distributed case,
        # copy files from remote node to local node and then test
        # However, copying remote files on windows machines without SCP is nontrivial
        if args.distributed:
            return

        for mo in MO:
            if mo == MO.DIRECT:
                continue
            NiraapadClient.niraapad_mo = mo
            serial = Serial(connect=False)
        self.niraapad_server.stop_tracing()
        trace_file = self.niraapad_server.get_trace_file()

        backend_instance_id = 0
        for trace_msg_type, trace_msg in Tracer.parse_file(trace_file):
            if trace_msg_type == "StartServerTraceMsg" \
                or trace_msg_type == "StopServerTraceMsg" \
                or trace_msg_type == "DeleteTraceMsg" \
                or trace_msg_type == "DeleteConnectionTraceMsg":
                continue
            backend_instance_id += 1
            self.assertEqual(trace_msg.req.backend_instance_id,
                             backend_instance_id)
            self.assertEqual(pickle.loads(trace_msg.req.args), ())
            self.assertEqual(pickle.loads(trace_msg.req.kwargs),
                             {'connect': False})
            self.assertEqual(
                trace_msg.resp,
                niraapad_pb2.InitializeResp(exception=pickle.dumps(None)))

    def test_tracing_2(self):
        # TODO Ideally, in the distributed case,
        # copy files from remote node to local node and then test
        # However, copying remote files on windows machines without SCP is nontrivial
        if args.distributed:
            return

        NiraapadClient.niraapad_mo = MO.VIA_MIDDLEBOX
        devices = Serial.list_devices()  # 0
        device_ports = Serial.list_device_ports()  # 1
        device_serials = Serial.list_device_serials()  # 2
        serial = Serial(connect=False)  # 3

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
            if trace_msg_type == "StartServerTraceMsg" \
                or trace_msg_type == "StopServerTraceMsg" \
                or trace_msg_type == "DeleteTraceMsg" \
                or trace_msg_type == "DeleteConnectionTraceMsg":
                continue
            if counter == 0:
                self.assertEqual(trace_msg_type, "StaticMethodTraceMsg")
                self.assertEqual(trace_msg.req.method_name, "list_devices")
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
                self.assertEqual(len(pickle.loads(trace_msg.resp.resp)),
                                 len(devices))
            elif counter == 1:
                self.assertEqual(trace_msg_type, "StaticMethodTraceMsg")
                self.assertEqual(trace_msg.req.method_name, "list_device_ports")
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
                self.assertEqual(
                    pickle.loads(trace_msg.resp.resp).sort(),
                    device_ports.sort())
            elif counter == 2:
                self.assertEqual(trace_msg_type, "StaticMethodTraceMsg")
                self.assertEqual(trace_msg.req.method_name,
                                 "list_device_serials")
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
                self.assertEqual(
                    pickle.loads(trace_msg.resp.resp).sort(),
                    device_serials.sort())
            elif counter == 3:
                self.assertEqual(trace_msg_type, "InitializeTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs),
                                 {'connect': False})
                self.assertEqual(
                    trace_msg.resp,
                    niraapad_pb2.InitializeResp(exception=pickle.dumps(None)))
            elif counter == 4:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
            elif counter == 5:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs),
                                 {'stop_bits': 3})
            elif counter == 6:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {
                    'stop_bits': 4,
                    'data_bits': 4
                })
            elif counter == 7:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {
                    'parity': 5,
                    'stop_bits': 5,
                    'data_bits': 5
                })
            elif counter == 8:
                self.assertEqual(trace_msg_type, "GenericMethodTraceMsg")
                self.assertEqual(trace_msg.req.backend_instance_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {
                    'baudrate': 6,
                    'parity': 6,
                    'stop_bits': 6,
                    'data_bits': 6
                })
            else:
                self.fail("Shoudn't happen!")
            counter += 1


class TestUR3ArmBackend(unittest.TestCase):

    def setUp(self):
        if args.secure == False:
            args.keysdir = None

        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir,
                                                  args.keysdir)
            self.niraapad_server.start()

        UR3Arm.connect_to_middlebox(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_init_vm(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
            ur3_arm = UR3Arm("192.168.236.128", gripper_base_port=30002)
            jointpositions = [-54.36, -60.60, -85.60, -52.12, 121.92, 50.02]
            ur3_arm.move_joints(jointpositions)
            self.assertEqual(
                [round(elem, 2) for elem in ur3_arm.joint_positions],
                [round(elem, 2) for elem in jointpositions])

            location = Location(x=50,
                                y=-160,
                                z=550,
                                rx=-118.9,
                                ry=56.53,
                                rz=-135.8)
            ur3_arm.move_to_location(location)
            self.assertEqual(ur3_arm.location, location)

            self.assertEqual(ur3_arm.joint_count, 6)

            time.sleep(2)

    def test_simple_init(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
            ur3_arm = UR3Arm(connect=False)

    def test_init(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
            ur3_arm = UR3Arm(connect=False)
            self.assertEqual(ur3_arm.default_velocity, 250)
            self.assertEqual(ur3_arm.max_velocity, 500)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost', connect=False)
            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 500)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             position_units=Units.METERS,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             position_units=Units.METERS,
                             default_joint_velocity=3,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             position_units=Units.METERS,
                             default_joint_velocity=3,
                             max_joint_velocity=4,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
            self.assertEqual(ur3_arm.gripper_default_force, 0.5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             position_units=Units.METERS,
                             default_joint_velocity=3,
                             max_joint_velocity=4,
                             gripper_default_velocity=5,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             position_units=Units.METERS,
                             default_joint_velocity=3,
                             max_joint_velocity=4,
                             gripper_default_velocity=5,
                             gripper_default_force=6,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(host='localhost',
                             default_velocity=1,
                             max_velocity=2,
                             position_units=Units.METERS,
                             default_joint_velocity=3,
                             max_joint_velocity=4,
                             gripper_default_velocity=5,
                             gripper_default_force=6,
                             gripper_id=7,
                             connect=False)
            self.assertEqual(ur3_arm.default_velocity, 1)
            self.assertEqual(ur3_arm.max_velocity, 2)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 5)
            self.assertEqual(ur3_arm.connected, False)

            ur3_arm = UR3Arm(connect=False,
                             gripper_id=1,
                             gripper_default_force=0.2,
                             gripper_default_velocity=0.3,
                             max_joint_velocity=0.4,
                             default_joint_velocity=0.5,
                             position_units=Units.RADIANS,
                             max_velocity=0.6,
                             default_velocity=0.7,
                             host='1.2.3.4')
            self.assertEqual(ur3_arm.default_velocity, 0.7)
            self.assertEqual(ur3_arm.max_velocity, 0.6)
            self.assertEqual(ur3_arm.default_joint_velocity,
                             ur3_arm.default_velocity)
            self.assertEqual(ur3_arm.gripper_default_velocity, 0.3)
            self.assertEqual(ur3_arm.connected, False)

    def test_exception_handling(self):
        for mo in MO:
            NiraapadClient.niraapad_mo = mo
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


class TestIKABackend(unittest.TestCase):

    def setUp(self):
        if args.secure == False:
            args.keysdir = None

        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir,
                                                  args.keysdir)
            self.niraapad_server.start()

        NiraapadClient.connect_to_middlebox(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_simple_init(self):

        # Importing MagneticStirrer here as opposed to at the top because
        # it invokes the Niraapad middlebox even before it's initialized
        from ika.errors import IKAError
        from ika.magnetic_stirrer import MagneticStirrer

        for mo in MO:
            if mo != MO.DIRECT_PLUS_MIDDLEBOX:
                continue
            NiraapadClient.niraapad_mo = mo
            with self.assertRaises(IKAError):
                magnetic_stirrer = MagneticStirrer(device_port='COM16')


class TestFaultTolerance(unittest.TestCase):

    def setUp(self):
        if args.secure == False:
            args.keysdir = None

        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir,
                                                  args.keysdir)
            self.niraapad_server.start()

        NiraapadClient.connect_to_middlebox(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_ur3_arm_init(self):
        NiraapadClient.niraapad_mo = MO.DIRECT_PLUS_MIDDLEBOX

        ur3_arm = UR3Arm(connect=False)
        self.assertEqual(ur3_arm.default_velocity, 250)
        self.assertEqual(ur3_arm.max_velocity, 500)
        self.assertEqual(ur3_arm.default_joint_velocity,
                         ur3_arm.default_velocity)
        self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
        self.assertEqual(ur3_arm.gripper_default_force, 0.5)
        self.assertEqual(ur3_arm.connected, False)

        ur3_arm = UR3Arm(host='localhost', default_velocity=1, connect=False)
        self.assertEqual(ur3_arm.default_velocity, 1)
        self.assertEqual(ur3_arm.max_velocity, 500)
        self.assertEqual(ur3_arm.default_joint_velocity,
                         ur3_arm.default_velocity)
        self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
        self.assertEqual(ur3_arm.gripper_default_force, 0.5)
        self.assertEqual(ur3_arm.connected, False)

        if args.distributed == False:
            self.niraapad_server.stop()
        disable_print()

        ur3_arm = UR3Arm(host='localhost',
                         default_velocity=1,
                         max_velocity=2,
                         connect=False)
        self.assertEqual(ur3_arm.default_velocity, 1)
        self.assertEqual(ur3_arm.max_velocity, 2)
        self.assertEqual(ur3_arm.default_joint_velocity,
                         ur3_arm.default_velocity)
        self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
        self.assertEqual(ur3_arm.gripper_default_force, 0.5)
        self.assertEqual(ur3_arm.connected, False)

        ur3_arm = UR3Arm(host='localhost',
                         default_velocity=1,
                         max_velocity=2,
                         position_units=Units.METERS,
                         connect=False)
        self.assertEqual(ur3_arm.default_velocity, 1)
        self.assertEqual(ur3_arm.max_velocity, 2)
        self.assertEqual(ur3_arm.default_joint_velocity,
                         ur3_arm.default_velocity)
        self.assertEqual(ur3_arm.gripper_default_velocity, 0.5)
        self.assertEqual(ur3_arm.gripper_default_force, 0.5)
        self.assertEqual(ur3_arm.connected, False)

        enable_print()


class TestProductionEnvironment(unittest.TestCase):

    def setUp(self):
        if args.secure == False:
            args.keysdir = None

        if args.distributed == False:
            self.niraapad_server = NiraapadServer(args.port, args.tracedir,
                                                  args.keysdir)
            self.niraapad_server.start()

        NiraapadClient.connect_to_middlebox(args.host, args.port, args.keysdir)

    def tearDown(self):
        if args.distributed == False:
            self.niraapad_server.stop()
            del self.niraapad_server

    def test_init(self):
        for mo in MO:
            if mo != MO.VIA_MIDDLEBOX: continue
            print("Mode:", mo)
            # c9 = MyC9Controller(device_serial='FT2FT5C1',
            #                     use_joystick=True,
            #                     connect=True)
            # n9 = N9Robot(c9)
            # n9.home()

            # sum = 0
            # for i in range(10):
            #     sum += c9.axis_current(0)
            # avg = sum / 10.0
            # print("Gripper base current is", avg)

            # print("Initializing TecanCAvro")
            # serial_cavro = c9.com(0, baudrate=9600)
            # dosing_pump = TecanCavro(serial_cavro,
            #                          address=1,
            #                          syringe_volume_ml=1)

            # print("Initializing mini IKA")
            # mini_heater_stirrer_port = 'COM6'
            # mini_heater_stirrer = MagneticStirrer(device_port=mini_heater_stirrer_port)

            # print("Initializing Quantos")
            # quan = ArduinoAugmentedQuantos('192.168.254.2', 7, logging_level=10)
            # quan.set_home_direction(0)

            # print("Initializing centrifuge")
            # from ur.components.ur3_centrifuge.ur3_centrifuge import UR3Centrifuge
            # ur3_centrifuge = UR3Centrifuge(arm)

            # print("Disconnecting C9")
            # c9.disconnect()
            # print("Done")

            # time.sleep(1)


def suite_c9():
    suite = unittest.TestSuite()
    suite.addTest(TestC9Controller('test_instance_type'))
    suite.addTest(TestC9Controller('test_device_methods'))
    suite.addTest(TestC9Controller('test_connection_methods'))
    suite.addTest(TestC9Controller('test_py_serial_device'))
    return suite


def suite_serial():
    suite = unittest.TestSuite()
    suite.addTest(TestN9Backend('test_class_variables'))
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
    suite.addTest(TestUR3ArmBackend('test_simple_init'))
    suite.addTest(TestUR3ArmBackend('test_exception_handling'))
    return suite


def suite_ika():
    suite = unittest.TestSuite()
    suite.addTest(TestIKABackend('test_simple_init'))
    return suite


def suite_fault_tolerance():
    suite = unittest.TestSuite()
    suite.addTest(TestFaultTolerance('test_ur3_arm_init'))
    return suite


def suite_production_environment():
    suite = unittest.TestSuite()
    suite.addTest(TestProductionEnvironment('test_init'))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite_c9())
    runner.run(suite_serial())
    runner.run(suite_ur3arm())
    runner.run(suite_ika())
    # runner.run(suite_fault_tolerance())
    runner.run(suite_production_environment())
