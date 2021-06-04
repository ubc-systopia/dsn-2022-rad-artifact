import os
import sys
import grpc
import time
import pickle
import unittest

from concurrent import futures

file_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(file_path)))

import niraapad.protos.n9_pb2 as n9_pb2
import niraapad.protos.n9_pb2_grpc as n9_pb2_grpc

from niraapad.middlebox.n9_server import N9Server
from niraapad.shared.ftdi_serial import Serial
from niraapad.shared.tracing import Tracer
from niraapad.shared.utils import *

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
    serial.set_parameters(stop_bits=3)
    serial.set_parameters(stop_bits=4, data_bits=4)
    serial.set_parameters(parity=5, stop_bits=5, data_bits=5)
    serial.set_parameters(baudrate=6, parity=6, stop_bits=6, data_bits=6)

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

        trace_path = file_path + "/../traces/"
        keys_path = file_path + "/../keys/"

        host = 'localhost'
        port = '1337'

        self.n9_server = N9Server(port, trace_path, keys_path)
        self.n9_server.start()
        Serial.start_n9_client(host, port, keys_path)

    def tearDown(self):
        self.n9_server.stop()
        del self.n9_server

    def test_static_methods(self):
        for mo in MO:
            Serial.mo = mo
            serial_devices_info = Serial.list_devices()
            device_ports = Serial.list_device_ports()
            device_serials = Serial.list_device_serials()

    def test_init(self):
        """
        I have not implemented individual getter methods over RPC for each
        attribute. So for now I will test each invocation manually by checking
        the output of a print statement on the server side. I will put in some
        assertions for the read_timeout and write_timeout properties, since
        getters for these are part of the API.
        By default, the print statement in DirectSerial.__init__ may be disabled
        or even missing (if we are using a pristine copy).
        """
        for mo in MO:
            Serial.mo = mo
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
        for mo in MO:
            Serial.mo = mo
            serial = Serial(connect=False)
            self.assertEqual(5, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            serial.read_timeout = 55
            self.assertEqual(55, serial.read_timeout)
            self.assertEqual(5, serial.write_timeout)
            serial.write_timeout = 55
            self.assertEqual(55, serial.read_timeout)
            self.assertEqual(55, serial.write_timeout)
            serial.read_timeout = 99
            self.assertEqual(99, serial.read_timeout)
            self.assertEqual(55, serial.write_timeout)
            serial.write_timeout = 33
            self.assertEqual(99, serial.read_timeout)
            self.assertEqual(33, serial.write_timeout)


    def test_set_parameters(self):
        """
        Like test_init above, I will verify these call manually using print
        statements on the server side.
        """
        for mo in MO:
            Serial.mo = mo
            serial = Serial(connect=False)
            serial.set_parameters(baudrate=10)
            serial.set_parameters(parity=11)
            serial.set_parameters(stop_bits=12)
            serial.set_parameters(data_bits=13)
            serial.set_parameters(baudrate=10, parity=11, stop_bits=12, data_bits=13)
            serial.set_parameters(baudrate=14, parity=15, stop_bits=16, data_bits=17)
            serial.set_parameters(baudrate=18, stop_bits=19)
            serial.set_parameters(parity=20, data_bits=21)

    def test_tracing_1(self):
        for mo in MO:
            if mo == MO.DIRECT_SERIAL: continue
            Serial.mo = mo
            serial = Serial(connect=False)
        self.n9_server.stop_tracing()
        trace_file = self.n9_server.get_trace_file()
        device_id = 0
        for trace_msg_type, trace_msg in Tracer.parse_file(trace_file):
            device_id += 1
            self.assertEqual(trace_msg.req.device_id, device_id)
            self.assertEqual(pickle.loads(trace_msg.req.args), ())
            self.assertEqual(pickle.loads(trace_msg.req.kwargs), {'connect': False})
            self.assertEqual(trace_msg.resp, n9_pb2.InitializeResp())

    def test_tracing_2(self):
        Serial.mo = MO.DIRECT_MIDDLEBOX
        devices = Serial.list_devices() # 0
        device_ports = Serial.list_device_ports() # 1
        device_serials = Serial.list_device_serials() # 2
        serial = Serial(connect=False) # 3
        serial.set_parameters() # 4
        serial.set_parameters(stop_bits=3) # 5
        serial.set_parameters(stop_bits=4, data_bits=4) # 6
        serial.set_parameters(parity=5, stop_bits=5, data_bits=5) #7
        serial.set_parameters(baudrate=6, parity=6, stop_bits=6, data_bits=6) # 8
        self.n9_server.stop_tracing()
        trace_file = self.n9_server.get_trace_file()
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
                self.assertEqual(trace_msg.req.device_id, 1)
                self.assertEqual(pickle.loads(trace_msg.req.args), ())
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {'connect': False})
                self.assertEqual(trace_msg.resp, n9_pb2.InitializeResp())
            elif counter == 4:
                self.assertEqual(trace_msg_type, "DeviceSpecificMethodTraceMsg")
                self.assertEqual(trace_msg.req.device_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {})
            elif counter == 5:
                self.assertEqual(trace_msg_type, "DeviceSpecificMethodTraceMsg")
                self.assertEqual(trace_msg.req.device_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs), {'stop_bits': 3})
            elif counter == 6:
                self.assertEqual(trace_msg_type, "DeviceSpecificMethodTraceMsg")
                self.assertEqual(trace_msg.req.device_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(pickle.loads(trace_msg.req.kwargs),
                                 {'stop_bits': 4, 'data_bits': 4})
            elif counter == 7:
                self.assertEqual(trace_msg_type, "DeviceSpecificMethodTraceMsg")
                self.assertEqual(trace_msg.req.device_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(
                    pickle.loads(trace_msg.req.kwargs),
                    {'parity': 5, 'stop_bits': 5, 'data_bits': 5})
            elif counter == 8:
                self.assertEqual(trace_msg_type, "DeviceSpecificMethodTraceMsg")
                self.assertEqual(trace_msg.req.device_id, 1)
                self.assertEqual(trace_msg.req.method_name, "set_parameters")
                self.assertEqual(
                    pickle.loads(trace_msg.req.kwargs),
                    {'baudrate': 6, 'parity': 6, 'stop_bits': 6, 'data_bits': 6})
            else:
                self.fail("Shoudn't happen!")
            counter += 1

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestN9Client('test_static_methods'))
    suite.addTest(TestN9Client('test_init'))
    suite.addTest(TestN9Client('test_setters_and_getters'))
    suite.addTest(TestN9Client('test_set_parameters'))
    suite.addTest(TestN9Client('test_tracing_1'))
    suite.addTest(TestN9Client('test_tracing_2'))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
