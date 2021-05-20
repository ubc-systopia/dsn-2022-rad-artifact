import grpc
import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.lab_computer.ftdi_serial import SerialDeviceInfo
from niraapad.shared.utils import *

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

    def list_devices(self):
        resp = self.stub.ListDevices(middlebox_pb2.EmptyMsg())
        unpacked = []
        for di in resp.devices_info:
            unpacked.append(SerialDeviceInfo(
                index=NoneIfEmptyString(di.index),
                serial=di.serial,
                port=NoneIfEmptyString(di.port),
                description=NoneIfEmptyString(di.description)))
        return unpacked

    def list_devices_trace(self, serial_devices_info):
        packed = []
        for di in serial_devices_info:
            packed.append(middlebox_pb2.SerialDeviceInfo(
                index=EmptyStringIfNone(di.index),
                serial=di.serial,
                port=EmptyStringIfNone(di.port),
                description=EmptyStringIfNone(di.description)))
        self.stub.ListDevicesTrace(middlebox_pb2.ListDevicesTraceMsg(
            resp=middlebox_pb2.ListDevicesResp(devices_info=packed)))

    def list_device_ports(self):
        resp = self.stub.ListDevicePorts(middlebox_pb2.EmptyMsg())
        return resp.ports

    def list_device_ports_trace(self, ports):
        self.stub.ListDevicePortsTrace(middlebox_pb2.ListDevicePortsTraceMsg(
            resp=middlebox_pb2.ListDevicePortsResp(ports=ports)))

    def list_device_serials(self):
        resp = self.stub.ListDeviceSerials(middlebox_pb2.EmptyMsg())
        return resp.serial_numbers

    def list_device_serials_trace(self, serial_numbers):
        self.stub.ListDeviceSerialsTrace(middlebox_pb2.ListDeviceSerialsTraceMsg(
            resp=middlebox_pb2.ListDeviceSerialsResp(serial_numbers=serial_numbers)))

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
        
        device = EmptyStringIfNone(device)
        device_type_format = middlebox_pb2.SerialDeviceType.Format.STRING
        if type(device) is int:
            device_type_format = middlebox_pb2.SerialDeviceType.Format.INT
            device = str(device)
        device_type = middlebox_pb2.SerialDeviceType(
          device_type_format=device_type_format, device_type=device)

        self.stub.Initialize(middlebox_pb2.InitializeReq(
            device_id=self.num_devices,
            device_type=device_type,
            device_serial=EmptyStringIfNone(device_serial),
            device_number=EmptyStringIfNone(device_number),
            device_port=EmptyStringIfNone(device_port),
            baudrate= baudrate,
            parity=parity,
            stop_bits=stop_bits,
            data_bits=data_bits,
            read_timeout=float(read_timeout),
            write_timeout=float(write_timeout),
            connect_timeout=float(connect_timeout),
            connect_retry=connect_retry,
            connect_settle_time=connect_settle_time,
            connect=connect))
        return self.num_devices

    def initialize_trace(self,
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
        
        device = EmptyStringIfNone(device)
        device_type_format = middlebox_pb2.SerialDeviceType.Format.STRING
        if type(device) is int:
            device_type_format = middlebox_pb2.SerialDeviceType.Format.INT
            device = str(device)
        device_type = middlebox_pb2.SerialDeviceType(
          device_type_format=device_type_format, device_type=device)

        self.stub.InitializeTrace(middlebox_pb2.InitializeTraceMsg(
                req=middlebox_pb2.InitializeReq(
                device_id=self.num_devices,
                device_type=device_type,
                device_serial=EmptyStringIfNone(device_serial),
                device_number=EmptyStringIfNone(device_number),
                device_port=EmptyStringIfNone(device_port),
                baudrate= baudrate,
                parity=parity,
                stop_bits=stop_bits,
                data_bits=data_bits,
                read_timeout=float(read_timeout),
                write_timeout=float(write_timeout),
                connect_timeout=float(connect_timeout),
                connect_retry=connect_retry,
                connect_settle_time=connect_settle_time,
                connect=connect)))

        return self.num_devices

    def open_device(self, device_id):
        self.stub.OpenDevice(middlebox_pb2.OpenDeviceReq(device_id=device_id))
    
    def open_device_trace(self, device_id):
        self.stub.OpenDeviceTrace(middlebox_pb2.OpenDeviceTraceMsg(
            req=middlebox_pb2.OpenDeviceReq(device_id=device_id)))
    
    def connect(self, device_id):
        self.stub.Connect(middlebox_pb2.ConnectReq(device_id=device_id))

    def connect_trace(self, device_id):
        self.stub.ConnectTrace(middlebox_pb2.ConnectTraceMsg(
            req=middlebox_pb2.ConnectReq(device_id=device_id)))

    def disconnect(self, device_id):
        self.stub.Disconnect(middlebox_pb2.DisconnectReq(device_id=device_id))

    def disconnect_trace(self, device_id):
        self.stub.DisconnectTrace(middlebox_pb2.DisconnectTraceMsg(
            req=middlebox_pb2.DisconnectReq(device_id=device_id)))

    def init_device(self, device_id):
        self.stub.InitDevice(middlebox_pb2.InitDeviceReq(device_id=device_id))

    def init_device_trace(self, device_id):
        self.stub.InitDeviceTrace(middlebox_pb2.InitDeviceTraceMsg(
            req=middlebox_pb2.InitDeviceReq(device_id=device_id)))

    def set_parameters(self, device_id, baudrate, parity, stop_bits, data_bits):
        self.stub.SetParameters(middlebox_pb2.SetParametersReq(
            device_id=device_id,
            baudrate=str(EmptyStringIfNone(baudrate)),
            parity=str(EmptyStringIfNone(parity)),
            stop_bits=str(EmptyStringIfNone(stop_bits)),
            data_bits=str(EmptyStringIfNone(data_bits))))

    def set_parameters_trace(self, device_id, baudrate, parity, stop_bits,
                             data_bits):
        self.stub.SetParametersTrace(middlebox_pb2.SetParametersTraceMsg(
            req=middlebox_pb2.SetParametersReq(
                device_id=device_id,
                baudrate=str(EmptyStringIfNone(baudrate)),
                parity=str(EmptyStringIfNone(parity)),
                stop_bits=str(EmptyStringIfNone(stop_bits)),
                data_bits=str(EmptyStringIfNone(data_bits)))))

    def update_timeouts(self, device_id):
        self.stub.UpdateTimeouts(middlebox_pb2.UpdateTimeoutsReq(
            device_id=device_id))

    def update_timeouts_trace(self, device_id):
        self.stub.UpdateTimeoutsTrace(middlebox_pb2.UpdateTimeoutsTraceMsg(
            req=middlebox_pb2.UpdateTimeoutsReq(device_id=device_id)))

    def info(self, device_id):
        resp = self.stub.Info(middlebox_pb2.InfoReq(device_id=device_id))
        di = resp.device_info
        return SerialDeviceInfo(
            index=NoneIfEmptyString(di.index),
            serial=di.serial,
            port=NoneIfEmptyString(di.port),
            description=NoneIfEmptyString(di.description))

    def info_trace(self, device_id, device_info):
        self.stub.InfoTrace(middlebox_pb2.InfoTraceMsg(
            req=middlebox_pb2.InfoReq(device_id=device_id),
            resp=middlebox_pb2.InfoResp(device_info=SerialDeviceInfo(
                index=EmptyStringIfNone(device_info.index),
                serial=deviec_info.serial,
                port=EmptyStringIfNone(device_info.port),
                description=EmptyStringIfNone(device_info.description)))))

    def serial_number(self, device_id):
        resp = self.stub.SerialNumber(middlebox_pb2.SerialNumberReq(
            device_id=device_id))
        return NoneIfEmptyString(resp.device_serial)

    def serial_number_trace(self, device_id, device_serial):
        self.stub.SerialNumberTrace(middlebox_pb2.SerialNumberTraceMsg(
            req=middlebox_pb2.SerialNumberReq(device_id=device_id),
            resp=middlebox_pb2.SerialNumberResp(device_serial=device_serial)))

    def in_waiting(self, device_id):
        resp = self.stub.InWaiting(middlebox_pb2.InWaitingReq(
            device_id=device_id))
        return resp.num_bytes

    def in_waiting_trace(self, device_id, num_bytes):
        self.stub.InWaitingTrace(middlebox_pb2.InWaitingTraceMsg(
            req=middlebox_pb2.InWaitingReq(device_id=device_id),
            resp=middlebox_pb2.InWaitingResp(num_bytes=num_bytes)))

    def out_waiting(self, device_id):
        resp = self.stub.OutWaiting(middlebox_pb2.OutWaitingReq(
            device_id=device_id))
        return resp.num_bytes

    def out_waiting_trace(self, device_id, num_bytes):
        self.stub.OutWaitingTrace(middlebox_pb2.OutWaitingTraceMsg(
            req=middlebox_pb2.OutWaitingReq(device_id=device_id),
            resp=middlebox_pb2.OutWaitingResp(num_bytes=num_bytes)))

    def read_timeout(self, device_id):
        resp = self.stub.ReadTimeout(middlebox_pb2.ReadTimeoutReq(
            device_id=device_id))
        return resp.timeout

    def read_timeout_trace(self, device_id, timeout):
        self.stub.ReadTimeoutTrace(middlebox_pb2.ReadTimeoutTraceMsg(
            req=middlebox_pb2.ReadTimeoutReq(device_id=device_id),
            resp=middlebox_pb2.ReadTimeoutResp(timeout=timeout)))

    def set_read_timeout(self, device_id, timeout):
        self.stub.ReadTimeout(middlebox_pb2.SetReadTimeoutReq(
            device_id=device_id, timeout=timeout))

    def set_read_timeout_trace(self, device_id):
        self.stub.SetReadTimeoutTrace(middlebox_pb2.SetReadTimeoutTraceMsg(
            req=middlebox_pb2.SetReadTimeoutReq(
                device_id=device_id, timeout=timeout)))

    def write_timeout(self, device_id):
        resp = self.stub.WriteTimeout(middlebox_pb2.WriteTimeoutReq(
            device_id=device_id))
        return resp.timeout

    def write_timeout_trace(self, device_id, timeout):
        self.stub.WriteTimeoutTrace(middlebox_pb2.WriteTimeoutTraceMsg(
            req=middlebox_pb2.WriteTimeoutReq(device_id=device_id),
            resp=middlebox_pb2.WriteTimeoutResp(timeout=timeout)))

    def set_write_timeout(self, device_id, timeout):
        self.stub.WriteTimeout(middlebox_pb2.SetWriteTimeoutReq(
            device_id=device_id, timeout=timeout))

    def set_write_timeout_trace(self, device_id):
        self.stub.SetWriteTimeoutTrace(middlebox_pb2.SetWriteTimeoutTraceMsg(
            req=middlebox_pb2.SetWriteTimeoutReq(
                device_id=device_id, timeout=timeout)))

    def read(self, device_id, num_bytes, timeout):
        resp = self.stub.Read(middlebox_pb2.ReadReq(
            device_id=device_id,
            num_bytes=EmptyStringIfNone(num_bytes),
            timeout=EmptyStringIfNone(timeout)))
        return resp.data

    def read_trace(self, device_id, num_bytes, timeout, data):
        self.stub.ReadTrace(middlebox_pb2.ReadTraceMsg(
            req=middlebox_pb2.ReadReq(
                device_id=device_id,
                num_bytes=EMptyStringIfNone(num_bytes),
                timeout=EmptyStringIfNone(timeout)),
            resp=middlebox_pb2.ReadResp(data=data)))

    def read_line(self, device_id, line_ending, timeout):
        resp = self.stub.ReadLine(middlebox_pb2.ReadLineReq(
            device_id=device_id,
            line_ending=line_ending,
            timeout=EmptyStringIfNone(timeout)))
        return resp.data

    def read_line_trace(self, device_id, line_ending, timeout, data):
        self.stub.ReadLineTrace(middlebox_pb2.ReadLineTraceMsg(
            req=middlebox_pb2.ReadLineReq(
                device_id=device_id,
                line_ending=line_ending,
                timeout=EmptyStringIfNone(timeout)),
            resp=middlebox_pb2.ReadLineResp(data=data)))

    def write(self, device_id, data, timeout):
        data_format = middlebox_pb2.WriteReq.Format.STRING
        if type(data) == bytes:
            data = data.decode()
            data_format = middlebox_pb2.WriteReq.Format.BYTES

        resp = self.stub.Write(middlebox_pb2.WriteReq(
            device_id=device_id,
            data_format=data_format,
            data=data,
            timeout=EmptyStringIfNone(timeout)))

        return resp.num_bytes

    def write_trace(self, device_id, data, timeout, num_bytes):
        data_format = middlebox_pb2.WriteReq.Format.STRING
        if type(data) == bytes:
            data = data.decode()
            data_format = middlebox_pb2.WriteReq.Format.BYTES

        self.stub.WriteTrace(middlebox_pb2.WriteTraceMsg(
            req=middlebox_pb2.WriteReq(
                device_id=device_id,
                data_format=data_format,
                data=data,
                timeout=EmptyStringIfNone(timeout)),
            resp=middlebox_pb2.WriteResp(num_bytes=num_bytes)))

    def request(self, device_id, write_data, timeout, line_ending):
        resp = self.stub.Request(middlebox_pb2.RequestReq(
            device_id=device_id,
            data=write_data,
            timeout=EmptyStringIfNone(timeout),
            line_ending=line_ending))
        return resp.data

    def request_trace(self, device_id, write_data, timeout, line_ending,
                      read_data):
        self.stub.RequestTrace(middlebox_pb2.RequestTraceMsg(
            req=middlebox_pb2.RequestReq(
                device_id=device_id,
                data=write_data,
                timeout=EmptyStringIfNone(timeout),
                line_ending=line_ending),
            resp=middlebox_pb2.RequestResp(data=read_data)))
    
    def flush(self, device_id):
        self.stub.Flush(middlebox_pb2.FlushReq(device_id=device_id))

    def flush_trace(self, device_id):
        self.stub.FlushTrace(middlebox_pb2.FlushTraceMsg(
            req=middlebox_pb2.FlushReq(device_id=device_id)))

    def reset_input_buffer(self, device_id):
        self.stub.ResetInputBuffer(middlebox_pb2.ResetInputBufferReq(
            device_id=device_id))

    def reset_input_buffer_trace(self, device_id):
        self.stub.ResetInputBufferTrace(middlebox_pb2.ResetInputBufferTraceMsg(
            req=middlebox_pb2.ResetInputBufferReq(device_id=device_id)))

    def reset_output_buffer(self, device_id):
        self.stub.ResetOutputBuffer(middlebox_pb2.ResetOutputBufferReq(
            device_id=device_id))

    def reset_output_buffer_trace(self, device_id):
        self.stub.ResetOutputBufferTrace(middlebox_pb2.ResetOutputBufferTraceMsg(
            req=middlebox_pb2.ResetOutputBufferReq(device_id=device_id)))

    def set_bit_mode(self, device_id, mask, enable):
        self.stub.SetBitMode(middlebox_pb2.SetBitModeReq(
            device_id=device_id, mask=mask, enable=enable))

    def set_bit_mode_trace(self, device_id, mask, enable):
        self.stub.SetBitModeTrace(middlebox_pb2.SetBitModeTraceMsg(
            req=middlebox_pb2.SetBitModeReq(
                device_id=device_id, mask=mask, enable=enable)))
