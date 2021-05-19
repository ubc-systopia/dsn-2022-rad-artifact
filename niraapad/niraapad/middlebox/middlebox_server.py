import grpc
from concurrent import futures

import niraapad.protos.middlebox_pb2 as middlebox_pb2
import niraapad.protos.middlebox_pb2_grpc as middlebox_pb2_grpc

from niraapad.middlebox.ftdi_serial import Serial

class MiddleboxServicer(middlebox_pb2_grpc.MiddleboxServicer):
    """Provides methods that implement functionality of middlebox server."""

    def __init__(self):
        print("MiddleboxServicer.__init__")
        self.serial_objs = {}

    def log_trace_msg(self, context, trace_msg):
        trace_msg_str = trace_msg.SerializeToString()
        print("%s: %s" % (context, trace_msg_str))

    def ListDevices(self, req, context):
        unpacked = Serial.list_devices()
        devices_info = []
        for di in unpacked:
            devices_info.append(middlebox_pb2.SerialDeviceInfo(
                index=EmptyStringIfNone(di.index),
                serial=di.serial,
                port=EmptyStringIfNone(di.port),
                description=EmptyStringIfNone(di.description))
        resp = middlebox_pb2.ListDevicesResp(devices_info=devices_info)
        trace_msg = middlebox_pb2.ListDevicesTraceMsg(resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def ListDevicePorts(self, req, context):
        resp = middlebox_pb2.ListDevicePortsResp(
            ports=Serial.list_device_ports())
        trace_msg = middlebox_pb2.ListDevicePortsTraceMsg(resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def ListDeviceSerials(self, req, context):
        serial_numbers = Serial.list_device_serials()
        resp = middlebox_pb2.ListDeviceSerials(
            serial_numbers= Serial.list_device_serials())
        trace_msg = middlebox_pb2.ListDeviceSerialsTraceMsg(resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def Initialize(self, req, context):
        device_type = req.device_type.device_type
        if device_type == "": device_type = None
        elif req.device_type.format == req.device_type.Format.INT:
            device_type = int(device_type)

        device_serial = req.device_serial if req.device_serial != "" else None
        device_number = int(req.device_number) if req.device_number != "" else None
        device_port = req.device_port if req.device_port != "" else None

        serial = Serial(device_type,
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

        resp = middlebox_pb2.InitializeResp()
        return resp

    def OpenDevice(self, req, context):
        self.serial_objs[req.device_id].open_device()
        trace_msg = middlebox_pb2.OpenDeviceTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)
        
    def Connect(self, req, context):
        self.serial_objs[req.device_id].connect()
        trace_msg = middlebox_pb2.ConnectTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def Disconnect(self, req, context):
        self.serial_objs[req.device_id].disconnect()
        trace_msg = middlebox_pb2.DisconnectTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def InitDevice(self, req, context):
        self.serial_objs[req.device_id].init_device()
        trace_msg = middlebox_pb2.InitDeviceTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)
        
    def SetParameters(self, req, context):
        self.serial_objs[req.device_id].set_parameters(
            baudrate=NoneIfEmptyString(req.baudrate),
            parity=NoneIfEmptyString(req.parity),
            stop_bits=NoneIfEmptyString(req.stop_bits),
            data_bits=NoneIfEmptyString(req.data_bits))
        trace_msg = middlebox_pb2.SetParametersTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def UpdateTimeouts(self, req, context):
        self.serial_objs[req.device_id].update_timeouts()
        trace_msg = middlebox_pb2.UpdateTimeoutsTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def Info(self, req, context):
        unpacked = self.serial_objs[req.device_id].info
        device_info = middlebox_pb2.SerialDeviceInfo(
            index=EmptyStringIfNone(unpacked.index),
            serial=EmptyStringIfNone(unpacked.serial),
            port=EmptyStringIfNone(unpacked.port),
            description=EmptyStringIfNone(unpacked.description))
        resp = middlebox_pb2.InfoResp(device_info=device_info)
        trace_msg = middlebox_pb2.InfoTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def SerialNumber(self, req, context):
        device_serial = self.serial_objs[req.device_id].serial_number
        resp = middlebox_pb2.SerialNumberResp(
            device_serial=EmptyStringIfNone(device_serial))
        trace_msg = middlebox_pb2.SerialNumberTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def InWaiting(self, req, context):
        resp = middlebox_pb2.InWaitingResp(
            num_bytes=self.serial_objs[req.device_id].in_waiting())
        trace_msg = middlebox_pb2.InWaitingTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def OutWaiting(self, req, context):
        resp = middlebox_pb2.OutWaitingResp(
            num_bytes=self.serial_objs[req.device_id].out_waiting())
        trace_msg = middlebox_pb2.OutWaitingTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def ReadTimeout(self, req, context):
        resp = middlebox_pb2.ReadTimeoutResp(
            timeout=self.serial_objs[req.device_id].read_timeout)
        trace_msg = middlebox_pb2.ReadTimeoutTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def SetReadTimeout(self, req, context):
        self.serial_objs[req.device_id].read_timeout = req.timeout
        trace_msg = middlebox_pb2.SetReadTimeoutTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def WriteTimeout(self, req, context):
        resp = middlebox_pb2.WriteTimeoutResp(
            timeout=self.serial_objs[req.device_id].write_timeout)
        trace_msg = middlebox_pb2.WriteTimeoutTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def SetWriteTimeout(self, req, context):
        self.serial_objs[req.device_id].write_timeout = req.timeout
        trace_msg = middlebox_pb2.SetWriteTimeoutTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def Read(self, req, context):
        resp = middlebox_pb2.ReadResp(
            data=self.serial_objs[req.device_id].read(
                num_bytes=NoneIfEmptyString(req.num_bytes),
                timeout=NoneIfEmptyString(req.timeout)))
        trace_msg = middlebox_pb2.ReadTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def ReadLine(self, req, context):
        resp = middlebox_pb2.ReadLineResp(
            data=self.serial_objs[req.device_id].read_line(
                line_ending=req.line_ending,
                timeout=NoneIfEmptyString(req.timeout)))
        trace_msg = middlebox_pb2.ReadLineTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def Write(self, req, context):
        data = req.data
        if req.data_format == middlebox_pb2.WriteRequest.Format.BYTES:
            data = req.data.encode()
        resp = middlebox_pb2.WriteResp(
            num_bytes=self.serial_objs[req.device_id].write(
                data=data,
                timeout=NoneIfEmptyString(req.timeout)))
        trace_msg = middlebox_pb2.WriteTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def Request(self, req, context):
        resp = middlebox_pb2.RequestResp(
            data=self.serial_objs[req.device_id].request(
                data=req.data,
                timeout=NoneIfEmptyString(req.timeout),
                line_ending=req.line_ending))
        trace_msg = middlebox_pb2.RequestTraceMsg(req=req, resp=resp)
        self.log_trace_msg(func_name(), trace_msg)
        return resp

    def Flush(self, req, context):
        self.serial_objs[req.device_id].flush()
        trace_msg = middlebox_pb2.FlushTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def ResetInputBuffer(self, req, context):
        self.serial_objs[req.device_id].reset_input_buffer()
        trace_msg = middlebox_pb2.ResetInputBufferTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def ResetOutputBuffer(self, req, context):
        self.serial_objs[req.device_id].reset_output_buffer()
        trace_msg = middlebox_pb2.ResetOutputBufferTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def SetBitMode(self, req, context):
        self.serial_objs[req.device_id].set_bit_mode(mask=mask, enable=enable)
        trace_msg = middlebox_pb2.SetBitModeTraceMsg(req=req)
        self.log_trace_msg(func_name(), trace_msg)

    def ListDevicesTrace(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def ListDevicePortsTrace(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def ListDeviceSerials(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Initialize(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def OpenDevice(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)
        
    def Connect(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Disconnect(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def InitDevice(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)
        
    def SetParameters(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def UpdateTimeouts(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Info(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def SerialNumber(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def InWaiting(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def OutWaiting(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def ReadTimeout(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def SetReadTimeout(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def WriteTimeout(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def SetWriteTimeout(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Read(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def ReadLine(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Write(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Request(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def Flush(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def ResetInputBuffer(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def ResetOutputBuffer(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

    def SetBitMode(self, trace_msg, context):
        self.log_trace_msg(func_name(), trace_msg)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    middlebox_pb2_grpc.add_MiddleboxServicer_to_server(MiddleboxServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == ' __main__':
    serve()
