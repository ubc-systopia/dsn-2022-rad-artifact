import unittest
import grpc
import time

from concurrent import futures

import os
import sys
file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(file_path)))

import niraapad.protos.n9_pb2 as n9_pb2
import niraapad.protos.n9_pb2_grpc as n9_pb2_grpc

from niraapad.middlebox.n9_server import N9Server
from niraapad.shared.ftdi_serial import Serial
from niraapad.shared.tracing import Tracer
from niraapad.shared.utils import *

def call_all_static_methods():
    # Test list_devices
    serial_devices_info = Serial.list_devices()

    # Test list_device_ports
    device_ports = Serial.list_device_ports()

    # Test list_device_serials
    device_serials = Serial.list_device_serials()

def call_all_instance_methods(serial):
    # Test open_device
    #serial.open_device()

    # Test connect
    # TODO Try with a serial cable
    # Currently, server throws an exception: FTD2XX package not installed
    #serial.connect()

    # Test disconnect
    serial.disconnect()

    # Test init_device
    serial.init_device()

    # Test set_parameters
    serial.set_parameters()
    serial.set_parameters(baudrate=115200, parity=0, stop_bits=1, data_bits=8)

    # Test update_timeouts
    serial.update_timeouts()

    # Test info
    serial_device_info = serial.info

    # Test serial_number
    serial_number = serial.serial_number

    # Test in_waiting
    num_bytes = serial.in_waiting

    # Test out_waiting
    num_bytes = serial.out_waiting
    
    # Test read_timeout (getter)
    read_timeout = serial.read_timeout

    # Test read_timeout (setter)
    serial.read_timeout = 13

    # Test write_timeout (getter)
    write_timeout = serial.write_timeout

    # Test write_timeout (setter)
    serial.write_timeout = 17

    # Test read
    output = serial.read()

    # Test read_line
    output = serial.read_line()

    # test write
    num_bytes = serial.write("From TestN9Client")

    # Test request
    output = serial.request("From TestN9Client".encode())

    # Test flush
    serial.flush()

    # Test reset_input_buffer
    serial.reset_input_buffer()

    # Test reset_output_buffer
    serial.reset_output_buffer()

    # Test set_bit_mode
    serial.set_bit_mode(0, False)

def parse_traces(trace_file):
    print("Parsing file", trace_file)
    for trace_msg in Tracer.parse_file(trace_file):
        print(trace_msg)

class TestN9Client(unittest.TestCase):

    def setUp(self):
        self.trace_path = file_path + "/../traces/"
        self.keys_path = file_path + "/../keys/"
        self.n9_server = N9Server(trace_path=self.trace_path,
                                  keys_path=self.keys_path)
        self.n9_server.start()

    def tearDown(self):
        self.n9_server.stop()
        pass

    def test_all_methods(self):
        Serial.mo = MO.DIRECT_MIDDLEBOX

        # Test all serial methods
        call_all_static_methods()

        # Test initialize
        serial = Serial(connect=False)

        # Test all instance methods
        call_all_instance_methods(serial)

        # Reset mode
        Serial.mo = MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING

        # Test all serial methods
        call_all_static_methods()

        # Test initialize
        serial = Serial(connect=False)

        # Test all instance methods
        call_all_instance_methods(serial)
    
        # Test recoring the traces from logs
        #self.n9_server.stop()
        self.n9_server.stop_tracing()
        parse_traces(Tracer.get_trace_file(self.trace_path))

if __name__ == "__main__":
    unittest.main()
