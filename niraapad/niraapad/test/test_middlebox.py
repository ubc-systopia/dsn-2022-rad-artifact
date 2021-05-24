import unittest
import grpc
import time

from concurrent import futures

import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.middlebox.middlebox_server import MiddleboxServer
from niraapad.middlebox.middlebox_server import MiddleboxServicer
from niraapad.shared.ftdi_serial import Serial
from niraapad.shared.utils import *

import os
file_path = os.path.dirname(os.path.abspath(__file__))

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

def parse_traces(trace_file):
    # If all trace files in a folder need to be parsed
    #trace_files = []
    #for root, dirs, files in os.walk(trace_path):
    #    for file in files:
    #        if(file.endswith(".log")):
    #            trace_files.append(os.path.join(root,file))
    #for trace_file in trace_files:

    print("Parsing trace file:" , trace_file)

    try:
        f = open(trace_file, "rb")
        # Get file size for termination
        f.seek(0, os.SEEK_END)
        file_size = f.tell() # bytes
        f.seek(0)

        while f.tell() < file_size and \
            f.tell() + MiddleboxServicer.trace_metadata_length <= file_size:

            trace_metadata_str = f.read(MiddleboxServicer.trace_metadata_length)
            trace_metadata = middlebox_pb2.TraceMetadata()
            trace_metadata.ParseFromString(trace_metadata_str)

            # Read the actual trace msg
            trace_msg_str = f.read(trace_metadata.num_bytes)

            # Parse the actual trace msg based on metadata
            #print("%s" % trace_metadata.func_name)
            if "ListDevices" in trace_metadata.func_name:
                msg = middlebox_pb2.ListDevicesTraceMsg()
                msg.ParseFromString(trace_msg_str)
                #print(msg)
            elif "ListDevicePorts" in trace_metadata.func_name:
                msg = middlebox_pb2.ListDevicePortsTraceMsg()
                msg.ParseFromString(trace_msg_str)
                #print(msg)
            # elif ... and so on for each API
            else:
                pass

    except Exception as e:
        print("Eception:", e)

    f.close()

class TestMiddleboxClient(unittest.TestCase):

    def setUp(self):
        self.trace_path = file_path + "/../traces/"
        self.keys_path = file_path + "/../keys/"
        self.middlebox_server = MiddleboxServer(trace_path=self.trace_path,
                                                keys_path=self.keys_path)
        self.middlebox_server.start()

    def tearDown(self):
        self.middlebox_server.stop()
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
        self.middlebox_server.stop()
        parse_traces(self.middlebox_server.trace_file)

if __name__ == "__main__":
    unittest.main()
