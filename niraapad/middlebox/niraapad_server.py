import os
import sys
import time
import grpc
import pickle

from concurrent import futures
from datetime import datetime

from ftdi_serial import Serial as DirectSerial
from hein_robots.universal_robots.ur3 import UR3Arm as DirectUR3Arm

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc

from niraapad.shared.utils import *
from niraapad.shared.tracing import Tracer

class NiraapadServicer(niraapad_pb2_grpc.NiraapadServicer):
    """Provides methods that implement functionality of n9 server."""

    trace_metadata_length = 132 # bytes

    def __init__(self, tracedir):
        self.backend_instances = {}
        self.tracer = Tracer(tracedir)

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

    def __init__(self, port, tracedir, keysdir):
        self.keysdir = keysdir
        server_key_path = os.path.join(self.keysdir, "server.key")
        server_crt_path = os.path.join(self.keysdir, "server.crt")
        print("server.key:", server_key_path)
        print("server.crt:", server_crt_path)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        print("NiraapadServer::__init__", port)
        with open(server_key_path, 'rb') as f:
            private_key = f.read()
        with open(server_crt_path, 'rb') as f:
            certificate_chain = f.read()
        server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )
        self.server.add_secure_port('[::]:' + str(port), server_credentials)

        self.niraapad_servicer = NiraapadServicer(tracedir=tracedir)
        niraapad_pb2_grpc.add_NiraapadServicer_to_server(self.niraapad_servicer, self.server)

    def start(self, wait=False):
        print("NiraapadServer::start")
        self.server.start()
        
        # cleanly blocks the calling thread until the server terminates
        if wait:
            print("NiraapadServer::start waiting for termination")
            self.server.wait_for_termination()

    def stop(self):
        print("NiraapadServer::stop")
        sys.stdout.flush()
        self.niraapad_servicer.stop_tracing()
        event = self.server.stop(None)
        event.wait()

    def stop_tracing(self):
        self.niraapad_servicer.stop_tracing()

    def get_trace_file(self):
        return self.niraapad_servicer.tracer.trace_file