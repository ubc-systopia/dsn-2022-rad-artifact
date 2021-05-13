import unittest
import grpc
import time

from concurrent import futures

import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.middlebox.middlebox_server import MiddleboxServicer
from niraapad.lab_computer.ftdi_serial import Serial as VirtualSerial

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

class TestMiddleboxClient(unittest.TestCase):

    def setUp(self):
        self.server = start_server()

    def tearDown(self):
        self.server.stop(None)

    def test_all_rpc_methods(self):

        # Test list_devices
        serial_devices_info = VirtualSerial.list_devices();
        print("Serial devices info:")
        for i in serial_devices_info: print(i)

        # Test list_device_ports
        device_ports = VirtualSerial.list_device_ports();
        print("Serial device ports:")
        for p in device_ports: print(p)

        # Test list_device_serials
        # TODO

        # Test initialize
        serial = VirtualSerial(connect=False)

        # Test connect
        # TODO Try with a serial cable
        # Currently, server throws an exception: FTD2XX package not installed
        #serial.connect()

        # Test disconnect
        serial.disconnect()

        # Test set_parameters
        serial.set_parameters()
        serial.set_parameters(baudrate=115200, parity=0, stop_bits=1, data_bits=8)

        # Test update_timeouts
        serial.update_timeouts()

        # Test info
        serial_device_info = serial.info
        print("Serial device info:", serial_device_info)

        # Test serial_number
        serial_number = serial.serial_number
        print("Device serial number:", serial_number)

        # Test read
        output = serial.read()
        print("Read output:", output.decode())

        # Test read_line
        output = serial.read_line()
        print("Read (line) output:", output.decode())

        # test write
        num_bytes = serial.write("From TestMiddleboxClient")
        print("Number of bytes written:", num_bytes)

        # Test request
        output = serial.request("From TestMiddleboxClient".encode())
        print("Request output:", output.decode())

if __name__ == "__main__":
    unittest.main()
