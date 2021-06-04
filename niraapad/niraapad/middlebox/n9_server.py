import os
import sys
import time
import grpc
import pickle

from concurrent import futures
from datetime import datetime

import niraapad.protos.n9_pb2 as n9_pb2
import niraapad.protos.n9_pb2_grpc as n9_pb2_grpc

from niraapad.shared.ftdi_serial import DirectSerial
from niraapad.shared.tracing import Tracer
from niraapad.shared.utils import *

file_path = os.path.dirname(os.path.abspath(__file__))
default_keys_path = file_path + "/../keys/"
default_trace_path = file_path + "/../traces/"

class N9Servicer(n9_pb2_grpc.N9Servicer):
    """Provides methods that implement functionality of n9 server."""

    trace_metadata_length = 132 # bytes
    direct_serial_class_name = "DirectSerial"

    def __init__(self, trace_path):
        self.serial_objs = {}
        self.tracer = Tracer(trace_path)

    def stop_tracing(self):
        self.tracer.stop_tracing()

    def log_trace_msg(self, trace_msg):
        self.tracer.write_to_file(trace_msg)

    def StaticMethod(self, req, context):
        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)
        fun_arg_names = eval("inspect.getfullargspec(" + \
                             N9Servicer.direct_serial_class_name + \
                             "." + \
                             req.method_name + \
                             ").args")
        method_call_string = generate_method_call_string(
            N9Servicer.direct_serial_class_name,
            req.method_name,
            fun_arg_names,
            args,
            kwargs)
        resp = eval(method_call_string)
        resp = n9_pb2.StaticMethodResp(resp=pickle.dumps(resp))
        trace_msg = n9_pb2.StaticMethodTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def StaticMethodTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return n9_pb2.EmptyMsg()

    def Initialize(self, req, context):
        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)
        arg_names = inspect.getfullargspec(DirectSerial.__init__).args
        init_call_string = generate_init_call_string(
            N9Servicer.direct_serial_class_name,
            arg_names,
            args,
            kwargs)
        self.serial_objs[req.device_id] = eval(init_call_string)
        resp = n9_pb2.InitializeResp()
        trace_msg = n9_pb2.InitializeTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def InitializeTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return n9_pb2.EmptyMsg()

    def DeviceSpecificMethod(self, req, context):
        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)
        fun_arg_names = eval("inspect.getfullargspec(" + \
                             N9Servicer.direct_serial_class_name + \
                             "." + \
                             req.method_name + \
                             ").args")
        method_call_string = generate_method_call_string(
            "self.serial_objs[req.device_id]",
            req.method_name,
            fun_arg_names,
            args,
            kwargs)
        resp = eval(method_call_string)
        resp = n9_pb2.DeviceSpecificMethodResp(resp=pickle.dumps(resp))
        trace_msg = n9_pb2.DeviceSpecificMethodTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def DeviceSpecificMethodTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return n9_pb2.EmptyMsg()

    def DeviceSpecificGetter(self, req, context):
        getter_call_string = generate_getter_call_string(
            "self.serial_objs[req.device_id]",
            req.property_name)
        resp = eval(getter_call_string)
        resp = n9_pb2.DeviceSpecificGetterResp(resp=pickle.dumps(resp))
        trace_msg = n9_pb2.DeviceSpecificGetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def DeviceSpecificGetterTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return n9_pb2.EmptyMsg()

    def DeviceSpecificSetter(self, req, context):
        value = pickle.loads(req.value)
        setter_call_string = generate_setter_call_string(
            "self.serial_objs[req.device_id]",
            req.property_name)
        exec(setter_call_string)
        resp = n9_pb2.DeviceSpecificSetterResp()
        trace_msg = n9_pb2.DeviceSpecificSetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)
        return resp

    def DeviceSpecificSetterTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return n9_pb2.EmptyMsg()
 
class N9Server:

    def __init__(self, port, trace_path=None, keys_path=None):

        self.keys_path = default_keys_path
        if keys_path != None: self.keys_path = keys_path

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        with open(self.keys_path + 'server.key', 'rb') as f:
            private_key = f.read()
        with open(self.keys_path + 'server.crt', 'rb') as f:
            certificate_chain = f.read()
        server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )
        self.server.add_secure_port('[::]:' + str(port), server_credentials)

        self.n9_servicer = N9Servicer(trace_path=trace_path)
        n9_pb2_grpc.add_N9Servicer_to_server(self.n9_servicer, self.server)

    def start(self):
        self.server.start()

    def stop(self):
        sys.stdout.flush()
        self.n9_servicer.stop_tracing()
        event = self.server.stop(None)
        event.wait()

    def stop_tracing(self):
        self.n9_servicer.stop_tracing()

    def get_trace_file(self):
        return self.n9_servicer.tracer.trace_file
