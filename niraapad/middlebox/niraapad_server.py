import os
import sys
import time
import grpc
import pickle
import inspect
import importlib

from concurrent import futures
from datetime import datetime

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc

from niraapad.shared.tracing import Tracer
import niraapad.shared.utils as utils

class NiraapadServicer(niraapad_pb2_grpc.NiraapadServicer):
    """Provides methods that implement functionality of n9 server."""

    trace_metadata_length = 132 # bytes

    def __init__(self, tracedir):
        self.backend_instances = {}
        self.tracer = Tracer(tracedir)

        trace_msg = niraapad_pb2.StartServerTraceMsg()
        self.tracer.write_to_file(trace_msg)

    def stop_tracing(self):
        trace_msg = niraapad_pb2.StopServerTraceMsg()
        self.tracer.write_to_file(trace_msg)
        self.tracer.stop_tracing()

    def log_trace_msg(self, trace_msg):
        self.tracer.write_to_file(trace_msg)

    def StaticMethod(self, req, context):
        print("%s.%s" % (req.backend_type, req.method_name))

        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)

        resp = None
        exception = None

        try:
            module_name = importlib.import_module(
                utils.BACKENDS.modules[req.backend_type])
            class_name = getattr(module_name, req.backend_type)
            resp = getattr(class_name, req.method_name)(*args, **kwargs)
        except Exception as e: exception = e
            
        resp = niraapad_pb2.StaticMethodResp(exception=pickle.dumps(exception),
                                             resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.StaticMethodTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticMethodTrace(self, trace_msg, context):
        print("(trace) %s.%s" % (trace_msg.req.backend_type, trace_msg.req.method_name))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def StaticGetter(self, req, context):
        print("%s.%s" % (req.backend_type, req.property_name))

        resp = None
        exception = None

        try:
            module_name = importlib.import_module(
                utils.BACKENDS.modules[req.backend_type])
            class_name = getattr(module_name, req.backend_type)
            resp = getattr(class_name, req.property_name)
        except Exception as e: exception = e
            
        resp = niraapad_pb2.StaticGetterResp(exception=pickle.dumps(exception),
                                             resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.StaticGetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticGetterTrace(self, trace_msg, context):
        print("(trace) %s.%s" % (trace_msg.req.backend_type, trace_msg.req.property_name))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def StaticSetter(self, req, context):
        print("%s.set_%s" % (req.backend_type, req.property_name))

        value = pickle.loads(req.value)

        resp = None
        exception = None

        try:
            module_name = importlib.import_module(
                utils.BACKENDS.modules[req.backend_type])
            class_name = getattr(module_name, req.backend_type)
            setattr(class_name, req.property_name, value)
        except Exception as e: exception = e
            
        resp = niraapad_pb2.StaticSetterResp(exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.StaticSetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticSetterTrace(self, trace_msg, context):
        print("(trace) %s.%s" % (trace_msg.req.backend_type, trace_msg.req.property_name))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def Initialize(self, req, context):
        print("%s.__init__" % (req.backend_type))

        # Since the __init__ function is invoked similar to static methods,
        # that is, it is invoked using the class name, this function is
        # analogous to the static_method function above, except that we do not
        # need a variable for the method name, which is known to be "__init__"
        # in this case.

        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)

        if req.backend_type not in self.backend_instances:
            self.backend_instances[req.backend_type] = {}

        exception = None

        try:
            module_name = importlib.import_module(
                utils.BACKENDS.modules[req.backend_type])
            class_name = getattr(module_name, req.backend_type)
            self.backend_instances[req.backend_type][req.backend_instance_id] = \
                class_name(*args, **kwargs)
        except Exception as e:
            exception = e

        resp = niraapad_pb2.InitializeResp(exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.InitializeTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def InitializeTrace(self, trace_msg, context):
        print("(trace) %s.__init__" % (trace_msg.req.backend_type))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def GenericMethod(self, req, context):
        print("%s.%s" % (req.backend_type, req.method_name))

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

        resp = None
        exception = None

        try:
            resp = getattr(
                self.backend_instances[req.backend_type][req.backend_instance_id],
                    req.method_name)(*args, **kwargs)
        except Exception as e: exception = e
            
        resp = niraapad_pb2.GenericMethodResp(exception=pickle.dumps(exception),
                                              resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.GenericMethodTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericMethodTrace(self, trace_msg, context):
        print("(trace) %s.%s" % (trace_msg.req.backend_type, trace_msg.req.method_name))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def GenericGetter(self, req, context):
        print("%s.%s" % (req.backend_type, req.property_name))

        # Getter functions are an extremely simplified version of GenericMethod
        # since they are interpreted not as functions but as variables, which
        # may be used in an expression; in this case, we simply return the
        # variable value.

        resp = None
        exception = None

        try:
            resp = getattr(
                self.backend_instances[req.backend_type][req.backend_instance_id],
                req.property_name)
        except Exception as e: exception = e

        resp = niraapad_pb2.GenericGetterResp(exception=pickle.dumps(exception),
                                              resp=pickle.dumps(resp))

        trace_msg = niraapad_pb2.GenericGetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericGetterTrace(self, trace_msg, context):
        print("(trace) %s.%s" % (trace_msg.req.backend_type, trace_msg.req.property_name))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def GenericSetter(self, req, context):
        print("%s.set_%s" % (req.backend_type, req.property_name))

        # Setter functions are the opposite of getter functions. They simply
        # assign the provided value to the specified property.

        value = pickle.loads(req.value)

        resp = None
        exception = None

        try:
            setattr(
                self.backend_instances[req.backend_type][req.backend_instance_id],
                req.property_name, value)
        except Exception as e: exception = e

        resp = niraapad_pb2.GenericSetterResp(exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.GenericSetterTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericSetterTrace(self, trace_msg, context):
        print("(trace) %s.set_%s" % (trace_msg.req.backend_type, trace_msg.req.property_name))

        self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()
 
class NiraapadServer:

    def __init__(self, port, tracedir, keysdir=None):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        if keysdir == None:
            self.server.add_insecure_port('[::]:' + str(port))

        else:
            self.keysdir = keysdir
            server_key_path = os.path.join(self.keysdir, "server.key")
            server_crt_path = os.path.join(self.keysdir, "server.crt")

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
