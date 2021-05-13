import grpc
import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.shared.utils import *

import os
file_path = os.path.dirname(os.path.abspath(__file__))
keys_path = file_path + "/../keys/"

class MiddleboxClient:
    """
    The MiddleboxClient class encapsulates a gRPC client, which forwards all calls
    from class Serial on Lab Computer to the middlebox, which in turn is connected to 
    the modules via actual serial communication. Unlike class Serial,
    there is only one global instance of class MiddleboxClient.
    """

    def __init__(self):

        # INSECURE channel
        #channel = grpc.insecure_channel('localhost:50051')
        #self.stub = middlebox_pb2_grpc.MiddleboxStub(channel)

        # SECURE channel
        with open(keys_path + 'server.crt', 'rb') as f:
            trusted_certs = f.read()
        client_credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        channel = grpc.secure_channel('localhost:1337', client_credentials)
        self.stub = middlebox_pb2_grpc.MiddleboxStub(channel)

        self.num_devices = 0

    def list_devices(self) -> List[SerialDeviceInfo]:
        """
        Get a list of SerialDeviceInfo instanes with information about serial devices connected to the middlebox

        :return: list of SerialDeviceInfo instances
        """
        request = middlebox_pb2.ListDevicesRequest()
        response = self.stub.ListDevices(request)
        unpacked_response = []
        for device_info in response.devices_info:
            index = None if device_info.index == "" else int(device_info.index)
            serial = device_info.serial
            port = None if device_info.port == "" else device_info.port
            description = None if device_info.description == "" else device_info.description
            unpacked_device_info = SerialDeviceInfo(index, serial, port, description)
            unpacked_response.append(unpacked_device_info)
            
        return unpacked_response

    def list_device_ports(self) -> List[str]:
        """
        Get a list of COM port strings for connected serial devices

        :return: List of COM port strings
        """
        request = middlebox_pb2.ListDevicePortsRequest()
        response = self.stub.ListDevicePorts(request)
        return response.ports

    def list_device_serials(self) -> List[str]:
        """
        Get a list of device serial numbers for connected FTDI devices

        :return: List of device serial number strings
        """
        request = middlebox_pb2.ListDeviceSerialsRequest()
        response = self.stub.ListDeviceSerials(request)
        return response.serial_numbers

    def initialize(self,
                   device,
                   device_serial,
                   device_number,
                   device_port,
                   baudrate,
                   parity,
                   stop_bits,
                   data_bits,
                   read_timeout,
                   write_timeout,
                   connect_timeout,
                   connect_retry,
                   connect_settle_time,
                   connect):
        self.num_devices += 1
        
        if device is None: device = ""
        device_type_format = middlebox_pb2.SerialDeviceType.Format.STRING
        if type(device) is int:
            device_type_format = middlebox_pb2.SerialDeviceType.Format.INT
            device = str(device)
        device_type = middlebox_pb2.SerialDeviceType(
          device_type_format=device_type_format, device_type=device)

        request = middlebox_pb2.InitializeRequest(
            device_id=self.num_devices,
            device_type=device_type,
            device_serial=(device_serial if device_serial != None else ""),
            device_number=(str(device_number) if device_number != None else ""),
            device_port=(device_port if device_port != None else ""),
            baudrate= baudrate,
            parity=parity,
            stop_bits=stop_bits,
            data_bits=data_bits,
            read_timeout=float(read_timeout),
            write_timeout=float(write_timeout),
            connect_timeout=float(connect_timeout),
            connect_retry=connect_retry,
            connect_settle_time=connect_settle_time,
            connect=connect)
        response = self.stub.Initialize(request)

        return self.num_devices
    
    def connect(self, device_id):
        request = middlebox_pb2.ConnectRequest(device_id=device_id)
        response = self.stub.Connect(request)

    def disconnect(self, device_id):
        request = middlebox_pb2.DisconnectRequest(device_id=device_id)
        response = self.stub.Disconnect(request)

    def set_parameters(self, device_id, baudrate, parity, stop_bits, data_bits):
        baudrate = str(baudrate) if baudrate != None else ""
        parity = str(parity) if parity != None else ""
        stop_bits = str(stop_bits) if stop_bits != None else ""
        data_bits = str(data_bits) if data_bits != None else ""
        request = middlebox_pb2.SetParametersRequest(device_id=device_id,
                                                     baudrate=baudrate,
                                                     parity=parity,
                                                     stop_bits=stop_bits,
                                                     data_bits=data_bits)
        response = self.stub.SetParameters(request)

    def update_timeouts(self, device_id):
        request = middlebox_pb2.UpdateTimeoutsRequest(device_id=device_id)
        response = self.stub.UpdateTimeouts(request)

    def info(self, device_id):
        request = middlebox_pb2.InfoRequest(device_id=device_id)
        response = self.stub.Info(request)
        return response.device_info

    def serial_number(self, device_id):
        request = middlebox_pb2.SerialNumberRequest(device_id=device_id)
        response = self.stub.SerialNumber(request)
        if response.device_serial == "": return None
        else: return response.device_serial

    def read(self, device_id, num_bytes, timeout):
        num_bytes = str(num_bytes) if num_bytes != None else ""
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.ReadRequest(device_id=device_id,
                                            num_bytes=num_bytes,
                                            timeout=timeout)
        response = self.stub.Read(request)
        return response.data

    def read_line(self, device_id, line_ending, timeout):
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.ReadLineRequest(device_id=device_id,
                                                line_ending=line_ending,
                                                timeout=timeout)
        response = self.stub.ReadLine(request)
        return response.data

    def write(self, device_id, data, timeout):
        timeout = str(timeout) if timeout != None else ""
        data_format = middlebox_pb2.WriteRequest.Format.STRING
        if type(data) == bytes:
            data = data.decode()
            data_format = middlebox_pb2.WriteRequest.Format.BYTES
        request = middlebox_pb2.WriteRequest(device_id=device_id,
                                             data_format=data_format,
                                             data=data,
                                             timeout=timeout)
        response = self.stub.Write(request)
        return response.num_bytes

    def request(self, device_id, data, timeout, line_ending):
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.RequestRequest(device_id=device_id,
                                              data=data,
                                              timeout=timeout,
                                              line_ending=line_ending)
        response = self.stub.Request(request)
        return response.data
