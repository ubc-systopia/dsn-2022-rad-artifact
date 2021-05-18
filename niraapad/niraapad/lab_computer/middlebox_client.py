import grpc
import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.lab_computer.ftdi_serial import SerialDeviceInfo
from niraapad.shared.utils import MO

import os
file_path = os.path.dirname(os.path.abspath(__file__))
keys_path = file_path + "/../keys/"

class MiddleboxClient:
    """
    The MiddleboxClient class encapsulates a gRPC client, which forwards all
    calls from class Serial on Lab Computer to the middlebox, which in turn is
    connected to the modules via actual serial communication. Unlike class
    Serial, there is only one global instance of class MiddleboxClient.
    """

    def __init__(self, mo):

        self.mo = mo

        # INSECURE channel
        #channel = grpc.insecure_channel('localhost:50051')
        #self.stub = middlebox_pb2_grpc.MiddleboxStub(channel)

        # SECURE channel
        with open(keys_path + 'server.crt', 'rb') as f:
            trusted_certs = f.read()
        client_credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs)
        channel = grpc.secure_channel('localhost:1337', client_credentials)
        self.stub = middlebox_pb2_grpc.MiddleboxStub(channel)

        self.num_devices = 0

    def list_devices(self, response):

        request = middlebox_pb2.ListDevicesRequest(mo=mo, response=response)
        response = self.stub.ListDevices(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        unpacked_response = []
        for device_info in response.devices_info:
            index = None if device_info.index == "" else int(device_info.index)
            serial = device_info.serial
            port = None if device_info.port == "" else device_info.port
            description = None if device_info.description == "" \
                else device_info.description
            unpacked_device_info = SerialDeviceInfo(
                index, serial, port, description)
            unpacked_response.append(unpacked_device_info)
        return unpacked_response

    def list_device_ports(self, response):

        request = middlebox_pb2.ListDevicePortsRequest(mo=mo, response=response)
        response = self.stub.ListDevicePorts(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.ports

    def list_device_serials(self, response):

        request = middlebox_pb2.ListDeviceSerialsRequest(mo=mo, response=response)
        response = self.stub.ListDeviceSerials(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.serial_numbers

    def initialize(self, response, device, device_serial, device_number,
                   device_port, baudrate, parity, stop_bits, data_bits,
                   read_timeout, write_timeout, connect_timeout, connect_retry,
                   connect_settle_time, connect):
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

    def open_device(self, response, device_id):
        request = middlebox_pb2.OpenDeviceRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.OpenDevice(request)
    
    def connect(self, response, device_id):
        request = middlebox_pb2.ConnectRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.Connect(request)

    def disconnect(self, response, device_id):
        request = middlebox_pb2.DisconnectRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.Disconnect(request)

    def init_device(self, response, device_id):
        request = middlebox_pb2.InitDevice(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.InitDevice(request)

    def set_parameters(self, response, device_id, baudrate, parity, stop_bits,
                       data_bits):
        request = middlebox_pb2.SetParametersRequest(
            mo=mo,
            response=response,
            device_id=device_id,
            baudrate=(str(baudrate) if baudrate != None else ""),
            parity=(str(parity) if parity != None else ""),
            stop_bits=(str(stop_bits) if stop_bits != None else ""),
            data_bits=(str(data_bits) if data_bits != None else ""))
        response = self.stub.SetParameters(request)

    def update_timeouts(self, response, device_id):
        request = middlebox_pb2.UpdateTimeoutsRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.UpdateTimeouts(request)

    def info(self, response, device_id):
        request = middlebox_pb2.InfoRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.Info(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.device_info

    def serial_number(self, response, device_id):
        request = middlebox_pb2.SerialNumberRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.SerialNumber(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        if response.device_serial == "":
            return None

        return response.device_serial

    def in_waiting(self, response, device_id):
        request = middlebox_pb2.InWaitingRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.InWaiting(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.num_bytes

    def out_waiting(self, response, device_id):
        request = middlebox_pb2.OutWaitingRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.OutWaiting(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.num_bytes

    def read_timeout(self, response, device_id):
        request = middlebox_pb2.ReadTimeoutRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.ReadTimeout(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.timeout

    def set_read_timeout(self, response, device_if, timeout):
        request = middlebox_pb2.ReadTimeoutRequest(
            mo=mo, response=response, device_id=device_id, timeout=timeout)
        response = self.stub.ReadTimeout(request)

    def write_timeout(self, response, device_id):
        request = middlebox_pb2.WriteTimeoutRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.WriteTimeout(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.timeout

    def set_write_timeout(self, response, device_if, timeout):
        request = middlebox_pb2.WriteTimeoutRequest(
            mo=mo, response=response, device_id=device_id, timeout=timeout)
        response = self.stub.WriteTimeout(request)

    def read(self, response, device_id, num_bytes, timeout):
        request = middlebox_pb2.ReadRequest(
            mo=mo,
            response=response,
            device_id=device_id,
            num_bytes=(str(num_bytes) if num_bytes != None else ""),
            timeout=(str(timeout) if timeout != None else ""))
        response = self.stub.Read(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.data

    def read_line(self, response, device_id, line_ending, timeout):
        request = middlebox_pb2.ReadLineRequest(
            mo=mo,
            response=response,
            device_id=device_id,
            line_ending=line_ending,
            timeout=(str(timeout) if timeout != None else ""))
        response = self.stub.ReadLine(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.data

    def write(self, response, device_id, data, timeout):
        data_format = middlebox_pb2.WriteRequest.Format.STRING
        if type(data) == bytes:
            data = data.decode()
            data_format = middlebox_pb2.WriteRequest.Format.BYTES

        request = middlebox_pb2.WriteRequest(
            mo=mo,
            response=response,
            device_id=device_id,
            data_format=data_format,
            data=data,
            timeout=(str(timeout) if timeout != None else ""))
        response = self.stub.Write(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.num_bytes

    def request(self, response, device_id, data, timeout, line_ending):
        request = middlebox_pb2.RequestRequest(
            mo=mo,
            response=response,
            device_id=device_id,
            data=data,
            timeout=(str(timeout) if timeout != None else ""),
            line_ending=line_ending)
        response = self.stub.Request(request)

        if mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING:
            return None

        return response.data
    
    def flush(self, response, device_id):
        request = middlebox_pb2.FlushRequest(
            mo=mo, response=response, device_id=device_id)
        response = self.stub.Flush(request)

    def reset_input_buffer(self, response, device_id):
        request = middlebox_pb2.ResetInputBufferRequest(
            mo=mo, response=response, device_id=device_id)
        reponse = self.stub.ResetInputBuffer(request)

    def reset_output_buffer(self, response, device_id):
        request = middlebox_pb2.ResetOutputBufferRequest(
            mo=mo, response=response, device_id=device_id)
        reponse = self.stub.ResetOutputBuffer(request)

    def set_bit_mode(self, response, device_id, mask, enable):
        request = middlebox_pb2.SetBitModeRequest(
            mo=mo, response=response, device_id=device_id, mask=mask, enable=enable)
        reponse = self.stub.ResetInputBuffer(request)
