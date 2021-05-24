import grpc
from concurrent import futures
from datetime import datetime

import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.shared.ftdi_serial import DirectSerial
from niraapad.shared.tracing import Tracer
from niraapad.shared.utils import *

import os
file_path = os.path.dirname(os.path.abspath(__file__))
default_keys_path = file_path + "/../keys/"
default_trace_path = file_path + "/../traces/"

class MiddleboxServicer(middlebox_pb2_grpc.MiddleboxServicer):
    """Provides methods that implement functionality of middlebox server."""

    trace_metadata_length = 132 # bytes

    def __init__(self, trace_path):
        print("MiddleboxServicer.__init__")
        self.serial_objs = {}
        self.tracer = Tracer(trace_path)

    def stop_tracing(self):
        self.tracer.stop_tracing()

    def log_trace_msg(self, trace_msg):
        self.tracer.write_to_file(trace_msg)

    def ListDevices(self, req, context):
        unpacked = DirectSerial.list_devices()
        devices_info = []
        for di in unpacked:
            devices_info.append(middlebox_pb2.SerialDeviceInfo(
                index=EmptyStringIfNone(di.index),
                serial=di.serial,
                port=EmptyStringIfNone(di.port),
                description=EmptyStringIfNone(di.description)))
        resp = middlebox_pb2.ListDevicesResp(devices_info=devices_info)
        trace_msg = middlebox_pb2.ListDevicesTraceMsg(resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def ListDevicePorts(self, req, context):
        resp = middlebox_pb2.ListDevicePortsResp(
            ports=DirectSerial.list_device_ports())
        trace_msg = middlebox_pb2.ListDevicePortsTraceMsg(resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def ListDeviceSerials(self, req, context):
        serial_numbers = DirectSerial.list_device_serials()
        resp = middlebox_pb2.ListDeviceSerialsResp(
            serial_numbers= DirectSerial.list_device_serials())
        trace_msg = middlebox_pb2.ListDeviceSerialsTraceMsg(resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def Initialize(self, req, context):
        device_type = req.device_type.device_type
        if device_type == "": device_type = None
        elif req.device_type.format == req.device_type.Format.INT:
            device_type = int(device_type)

        device_serial = req.device_serial if req.device_serial != "" else None
        device_number = int(req.device_number) if req.device_number != "" else None
        device_port = req.device_port if req.device_port != "" else None

        serial = DirectSerial(device_type,
                              device_serial,
                              device_number,
                              device_port,
                              req.baudrate,
                              req.parity,
                              req.stop_bits,
                              req.data_bits,
                              req.read_timeout,
                              req.write_timeout,
                              req.connect_timeout,
                              req.connect_retry,
                              req.connect_settle_time,
                              req.connect)

        self.serial_objs[req.device_id] = serial
        trace_msg = middlebox_pb2.InitializeTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def OpenDevice(self, req, context):
        self.serial_objs[req.device_id].open_device()
        trace_msg = middlebox_pb2.OpenDeviceTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()
        
    def Connect(self, req, context):
        self.serial_objs[req.device_id].connect()
        trace_msg = middlebox_pb2.ConnectTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def Disconnect(self, req, context):
        self.serial_objs[req.device_id].disconnect()
        trace_msg = middlebox_pb2.DisconnectTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def InitDevice(self, req, context):
        self.serial_objs[req.device_id].init_device()
        trace_msg = middlebox_pb2.InitDeviceTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()
        
    def SetParameters(self, req, context):
        self.serial_objs[req.device_id].set_parameters(
            baudrate=NoneIfEmptyString(req.baudrate),
            parity=NoneIfEmptyString(req.parity),
            stop_bits=NoneIfEmptyString(req.stop_bits),
            data_bits=NoneIfEmptyString(req.data_bits))
        trace_msg = middlebox_pb2.SetParametersTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def UpdateTimeouts(self, req, context):
        self.serial_objs[req.device_id].update_timeouts()
        trace_msg = middlebox_pb2.UpdateTimeoutsTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def Info(self, req, context):
        unpacked = self.serial_objs[req.device_id].info
        device_info = middlebox_pb2.SerialDeviceInfo(
            index=EmptyStringIfNone(unpacked.index),
            serial=EmptyStringIfNone(unpacked.serial),
            port=EmptyStringIfNone(unpacked.port),
            description=EmptyStringIfNone(unpacked.description))
        resp = middlebox_pb2.InfoResp(device_info=device_info)
        trace_msg = middlebox_pb2.InfoTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def SerialNumber(self, req, context):
        resp = middlebox_pb2.SerialNumberResp(
            device_serial=EmptyStringIfNone(
                self.serial_objs[req.device_id].serial_number))
        trace_msg = middlebox_pb2.SerialNumberTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def InWaiting(self, req, context):
        resp = middlebox_pb2.InWaitingResp(
            num_bytes=self.serial_objs[req.device_id].in_waiting)
        trace_msg = middlebox_pb2.InWaitingTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def OutWaiting(self, req, context):
        resp = middlebox_pb2.OutWaitingResp(
            num_bytes=self.serial_objs[req.device_id].out_waiting)
        trace_msg = middlebox_pb2.OutWaitingTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def ReadTimeout(self, req, context):
        resp = middlebox_pb2.ReadTimeoutResp(
            timeout=self.serial_objs[req.device_id].read_timeout)
        trace_msg = middlebox_pb2.ReadTimeoutTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def SetReadTimeout(self, req, context):
        self.serial_objs[req.device_id].read_timeout = req.timeout
        trace_msg = middlebox_pb2.SetReadTimeoutTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def WriteTimeout(self, req, context):
        resp = middlebox_pb2.WriteTimeoutResp(
            timeout=self.serial_objs[req.device_id].write_timeout)
        trace_msg = middlebox_pb2.WriteTimeoutTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def SetWriteTimeout(self, req, context):
        self.serial_objs[req.device_id].write_timeout = req.timeout
        trace_msg = middlebox_pb2.SetWriteTimeoutTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def Read(self, req, context):
        resp = middlebox_pb2.ReadResp(
            data=self.serial_objs[req.device_id].read(
                num_bytes=NoneIfEmptyString(req.num_bytes),
                timeout=NoneIfEmptyString(req.timeout)))
        trace_msg = middlebox_pb2.ReadTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def ReadLine(self, req, context):
        resp = middlebox_pb2.ReadLineResp(
            data=self.serial_objs[req.device_id].read_line(
                line_ending=req.line_ending,
                timeout=NoneIfEmptyString(req.timeout)))
        trace_msg = middlebox_pb2.ReadLineTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def Write(self, req, context):
        data = req.data
        if req.data_format == middlebox_pb2.WriteReq.Format.BYTES:
            data = req.data.encode()
        resp = middlebox_pb2.WriteResp(
            num_bytes=self.serial_objs[req.device_id].write(
                data=data,
                timeout=NoneIfEmptyString(req.timeout)))
        trace_msg = middlebox_pb2.WriteTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def Request(self, req, context):
        resp = middlebox_pb2.RequestResp(
            data=self.serial_objs[req.device_id].request(
                data=req.data,
                timeout=NoneIfEmptyString(req.timeout),
                line_ending=req.line_ending))
        trace_msg = middlebox_pb2.RequestTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def Flush(self, req, context):
        self.serial_objs[req.device_id].flush()
        trace_msg = middlebox_pb2.FlushTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ResetInputBuffer(self, req, context):
        self.serial_objs[req.device_id].reset_input_buffer()
        trace_msg = middlebox_pb2.ResetInputBufferTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ResetOutputBuffer(self, req, context):
        self.serial_objs[req.device_id].reset_output_buffer()
        trace_msg = middlebox_pb2.ResetOutputBufferTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def SetBitMode(self, req, context):
        self.serial_objs[req.device_id].set_bit_mode(
            mask=req.mask, enable=req.enable)
        trace_msg = middlebox_pb2.SetBitModeTraceMsg(req=req)
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ListDevicesTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ListDevicePortsTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ListDeviceSerialsTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def InitializeTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def OpenDeviceTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()
        
    def ConnectTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def DisconnectTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def InitDeviceTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()
        
    def SetParametersTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def UpdateTimeoutsTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def InfoTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def SerialNumberTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def InWaitingTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def OutWaitingTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ReadTimeoutTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def SetReadTimeoutTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def WriteTimeoutTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def SetWriteTimeoutTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ReadTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ReadLineTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def WriteTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def RequestTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def FlushTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ResetInputBufferTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def ResetOutputBufferTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

    def SetBitModeTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return middlebox_pb2.EmptyMsg()

#def serve():
#    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#    middlebox_pb2_grpc.add_MiddleboxServicer_to_server(MiddleboxServicer(), server)
#    server.add_insecure_port('[::]:50051')
#    server.start()
#    server.wait_for_termination()
#
#if __name__ == ' __main__':
#    serve()
 
class MiddleboxServer:

    def __init__(self, trace_path=None, keys_path=None):

        self.keys_path = default_keys_path
        if keys_path != None: self.keys_path = keys_path

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        with open(self.keys_path + 'server.key', 'rb') as f:
            private_key = f.read()
        with open(self.keys_path + 'server.crt', 'rb') as f:
            certificate_chain = f.read()
        server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )
        self.server.add_secure_port('[::]:1337', server_credentials)

        self.middlebox_servicer = MiddleboxServicer(trace_path=trace_path)
        middlebox_pb2_grpc.add_MiddleboxServicer_to_server(self.middlebox_servicer, self.server)
    
    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop(None)

    def stop_tracing(self):
        self.middlebox_servicer.stop_tracing()
