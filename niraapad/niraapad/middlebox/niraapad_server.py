import os
import sys
import time
import grpc
import pickle

from concurrent import futures
from datetime import datetime

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc

from niraapad.shared.ur3 import DirectUR3Arm
from niraapad.shared.ftdi_serial import DirectSerial
from niraapad.shared.tracing import Tracer
from niraapad.shared.utils import *

file_path = os.path.dirname(os.path.abspath(__file__))
default_keys_path = file_path + "/../keys/"
default_trace_path = file_path + "/../traces/"

class NiraapadServicer(niraapad_pb2_grpc.NiraapadServicer):
    """Provides methods that implement functionality of n9 server."""

    trace_metadata_length = 132 # bytes

    def __init__(self, trace_path):
        self.backend_instances = {}
        self.tracer = Tracer(trace_path)

    def stop_tracing(self):
        self.tracer.stop_tracing()

    def log_trace_msg(self, trace_msg):
        self.tracer.write_to_file(trace_msg)

    def StaticMethod(self, req, context):
        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)

        # For example, if the method invoked is DirectSerial.list_devices(...),
        # then we want to find the list of arguments (in string form) that the
        # method takes, which we can compute using Python's getfullargspec
        # method, i.e., using
        # "inspect.getfullargsepc(DirectSerial.list_devices).args". We generate
        # and evaluate this command automatically, as follows.
        func_arg_names = eval("inspect.getfullargspec(%s.%s).args" % \
                              (req.backend_type, req.method_name))

        # We want to invoke the respective static method in the original class,
        # say DirectSerial.list_devices(...). In order to do so automatically,
        # we generate and evaluate the method call string
        # "DirectSerial.list_devices(...)" automatically.
        method_call_string = generate_method_call_string(
            req.backend_type, req.method_name, func_arg_names, args, kwargs)

        resp = None
        exception = None

        try: resp = eval(method_call_string)
        except Exception as e: exception = e
            
        resp = niraapad_pb2.StaticMethodResp(exception=pickle.dumps(exception),
                                             resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.StaticMethodTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticMethodTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def Initialize(self, req, context):
        # Since the __init__ function is invoked similar to static methods,
        # that is, it is invoked using the class name, this function is
        # analogous to the static_method function above, except that we do not
        # need a variable for the method name, which is known to be "__init__"
        # in this case.

        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)

        arg_names = eval("inspect.getfullargspec(%s.__init__).args" % \
                         req.backend_type)

        init_call_string = generate_init_call_string(
            req.backend_type, arg_names, args, kwargs)

        if req.backend_type not in self.backend_instances:
            self.backend_instances[req.backend_type] = {}

        exception = None

        try:
            self.backend_instances[req.backend_type][req.backend_instance_id] = \
                eval(init_call_string)
        except Exception as e:
            exception = e

        resp = niraapad_pb2.InitializeResp(exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.InitializeTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def InitializeTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def GenericMethod(self, req, context):
        # For any generic class instance method, the logic is similar to that
        # of any generic static method, except that the method is invoked using
        # the class instance name and not directly using the class name.
        # Thus, the following set of statements is analogous to the function
        # definition of the static_methods function above, except that we deal
        # with specific class instances identified using their unique
        # identifiers ("backend_instance_id"), which were set during
        # initialization.

        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)

        func_arg_names = eval("inspect.getfullargspec(%s.%s).args" % \
                              (req.backend_type, req.method_name))

        backend_instance_str = \
            "self.backend_instances[req.backend_type][req.backend_instance_id]"
        method_call_string = generate_method_call_string(
            backend_instance_str, req.method_name, func_arg_names, args, kwargs)

        resp = None
        exception = None

        try: resp = eval(method_call_string)
        except Exception as e: exception = e
            
        resp = niraapad_pb2.GenericMethodResp(exception=pickle.dumps(exception),
                                              resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.GenericMethodTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericMethodTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def GenericGetter(self, req, context):
        # Getter functions are an extremely simplified version of GenericMethod
        # since they are interpreted not as functions but as variables, which
        # may be used in an expression; in this case, we simply return the
        # variable value.

        backend_instance_str = \
            "self.backend_instances[req.backend_type][req.backend_instance_id]"
        getter_call_string = generate_getter_call_string(backend_instance_str,
                                                         req.property_name)

        resp = None
        exception = None

        try: resp = eval(getter_call_string)
        except Exception as e: exception = e

        resp = niraapad_pb2.GenericGetterResp(exception=pickle.dumps(exception),
                                              resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.GenericGetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericGetterTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def GenericSetter(self, req, context):
        # Setter functions are the opposite of getter functions. They simply
        # assign the provided value to the specified property.

        value = pickle.loads(req.value)

        backend_instance_str = \
            "self.backend_instances[req.backend_type][req.backend_instance_id]"
        setter_call_string = generate_setter_call_string(backend_instance_str,
                                                         req.property_name)

        resp = None
        exception = None

        # We use an exec here instead of eval because assignment is a statement
        # and not an expression that can be evaluated.
        try: exec(setter_call_string)
        except Exception as e: exception = e

        resp = niraapad_pb2.GenericSetterResp(exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.GenericSetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericSetterTrace(self, trace_msg, context):
        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()
 
class NiraapadServer:

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

        self.niraapad_servicer = NiraapadServicer(trace_path=trace_path)
        niraapad_pb2_grpc.add_NiraapadServicer_to_server(self.niraapad_servicer, self.server)

    def start(self):
        self.server.start()

    def stop(self):
        sys.stdout.flush()
        self.niraapad_servicer.stop_tracing()
        event = self.server.stop(None)
        event.wait()

    def stop_tracing(self):
        self.niraapad_servicer.stop_tracing()

    def get_trace_file(self):
        return self.niraapad_servicer.tracer.trace_file
