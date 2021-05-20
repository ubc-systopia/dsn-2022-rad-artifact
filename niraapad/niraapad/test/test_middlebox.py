import unittest
import grpc
import time

from concurrent import futures

import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.middlebox.middlebox_server import MiddleboxServicer
from niraapad.lab_computer.ftdi_serial import Serial
from niraapad.shared.utils import *

import os
file_path = os.path.dirname(os.path.abspath(__file__))
keys_path = file_path + "/../keys/"

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # INSECURE channel
    #server.add_insecure_port('[::]:50051')

    # SECURE channel
    with open(keys_path + 'server.key', 'rb') as f:
        private_key = f.read()
    with open(keys_path + 'server.crt', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )
    server.add_secure_port('[::]:1337', server_credentials)

    middlebox_pb2_grpc.add_MiddleboxServicer_to_server(MiddleboxServicer(), server)
    server.start()
    #time.sleep(200)

    return server

def call_all_static_methods():
    # Check mode
    print("Operation mode:", Serial.mo)

    # Test list_devices
    serial_devices_info = Serial.list_devices()

    # Test list_device_ports
    device_ports = Serial.list_device_ports()

    # Test list_device_serials
    device_serials = Serial.list_device_serials()

def call_all_instance_methods(serial):
    # Check mode
    print("Operation mode:", Serial.mo)

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
    num_bytes = serial.write("From TestMiddleboxClient")

    # Test request
    output = serial.request("From TestMiddleboxClient".encode())

    # Test flush
    serial.flush()

    # Test reset_input_buffer
    serial.reset_input_buffer()

    # Test reset_output_buffer
    serial.reset_output_buffer()

    # Test set_bit_mode
    serial.set_bit_mode(0, False)

class TestMiddleboxClient(unittest.TestCase):

    def setUp(self):
        self.server = start_server()

    def tearDown(self):
        self.server.stop(None)

    def test_all_methods(self):
        # Set and check mode
        Serial.mo = MO.DIRECT_MIDDLEBOX
        print("Operation mode:", Serial.mo)

        # Test all serial methods
        call_all_static_methods()

        # Test initialize
        serial = Serial(connect=False)

        # Test all instance methods
        call_all_instance_methods(serial)

        # Reset and check mode
        Serial.mo = MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING
        print("Operation mode:", Serial.mo)

        # Test all serial methods
        call_all_static_methods()

        # Test initialize
        serial = Serial(connect=False)

        # Test all instance methods
        call_all_instance_methods(serial)

if __name__ == "__main__":
    unittest.main()
