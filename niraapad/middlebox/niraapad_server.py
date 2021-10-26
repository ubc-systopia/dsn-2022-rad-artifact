from math import isnan
import os
import sys
import time
import grpc
import pickle
import inspect
import importlib

from concurrent import futures
from datetime import datetime
from timeit import default_timer

from ftdi_serial import Device
from ftdi_serial import FtdiDevice
from ftdi_serial import PySerialDevice

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc

from niraapad.shared.tracing import Tracer
import niraapad.shared.utils as utils

niraapad_backends_module = importlib.import_module("niraapad.backends")


class NiraapadServicer(niraapad_pb2_grpc.NiraapadServicer):
    """Provides methods that implement functionality of n9 server."""

    trace_metadata_length = 132  # bytes

    def __init__(self, tracedir):
        print("Initializing NiraapadServicer", flush=True)
        self.backend_instances = {}
        self.tracer = Tracer(tracedir)

        trace_msg = niraapad_pb2.StartServerTraceMsg()
        self.tracer.write_to_file(trace_msg)

    def stop_tracing(self):
        trace_msg = niraapad_pb2.StopServerTraceMsg()
        self.tracer.write_to_file(trace_msg)
        self.tracer.stop_tracing()

    def log_trace_msg(self, trace_msg, elapsed=0):
        self.tracer.write_to_file(trace_msg)

    def BatchedTrace(self, batched_trace_msg, context):
        trace_msgs = pickle.loads(batched_trace_msg.trace_msgs)
        for trace_msg in trace_msgs:
            print("(trace) %s.%s" %
                  (trace_msg.req.backend_type, Tracer.get_msg_type(trace_msg)))
            self.log_trace_msg(trace_msg)
        return niraapad_pb2.EmptyMsg()

    def InitializeConnection(self, req, context):
        print("NiraapadClientHelper.__init__", flush=True)

        resp = None
        exception = None

        resp = niraapad_pb2.InitializeConnectionResp(
            exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.InitializeConnectionTraceMsg(req=req,
                                                              resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def DeleteConnection(self, req, context):
        print("NiraapadClientHelper.__del__", flush=True)

        exception = None

        try:
            for backend_type in self.backend_instances:
                for backend_instance_id in self.backend_instances[backend_type]:
                    if backend_type == utils.BACKENDS.DEVICE \
                        or backend_type == utils.BACKENDS.MOCK_DEVICE \
                        or backend_type == utils.BACKENDS.FTDI_DEVICE \
                        or backend_type == utils.BACKENDS.PY_SERIAL_DEVICE:
                        self.backend_instances[backend_type][
                            backend_instance_id].close()
                    elif backend_type == utils.BACKENDS.ROBOT_ARM \
                        or backend_type == utils.BACKENDS.UR3_ARM:
                        if self.backend_instances[backend_type][
                                backend_instance_id].connected:
                            self.backend_instances[backend_type][
                                backend_instance_id].disconnect()
                    elif backend_type == utils.BACKENDS.BALANCE \
                        or backend_type == utils.BACKENDS.QUANTOS \
                        or backend_type == utils.BACKENDS.ARDUINO_AUGMENT \
                        or backend_type == utils.BACKENDS.ARDUINO_AUGMENTED_QUANTOS:
                        pass
            del self.backend_instances
            self.backend_instances = {}
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e

        resp = niraapad_pb2.DeleteConnectionResp(
            exception=pickle.dumps(exception))

        trace_msg = niraapad_pb2.DeleteConnectionTraceMsg(req=req, resp=resp)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticMethod(self, req, context):
        print("%s.%s" % (req.backend_type, req.method_name), flush=True)

        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)

        resp = None
        exception = None

        start = default_timer()
        try:
            class_name = getattr(niraapad_backends_module, req.backend_type)
            resp = getattr(class_name, req.method_name)(*args, **kwargs)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = utils.sanitize_resp(req.method_name, resp)

        resp = niraapad_pb2.StaticMethodResp(exception=pickle.dumps(exception),
                                             resp=pickle.dumps(resp))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.StaticMethodTraceMsg(req=req,
                                                      resp=resp,
                                                      profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticGetter(self, req, context):
        print("%s.get_%s" % (req.backend_type, req.property_name), flush=True)

        resp = None
        exception = None

        start = default_timer()
        try:
            class_name = getattr(niraapad_backends_module, req.backend_type)
            resp = getattr(class_name, req.property_name)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = niraapad_pb2.StaticGetterResp(exception=pickle.dumps(exception),
                                             resp=pickle.dumps(resp))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.StaticGetterTraceMsg(req=req,
                                                      resp=resp,
                                                      profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def StaticSetter(self, req, context):
        print("%s.set_%s" % (req.backend_type, req.property_name), flush=True)

        value = pickle.loads(req.value)

        resp = None
        exception = None

        start = default_timer()
        try:
            class_name = getattr(niraapad_backends_module, req.backend_type)
            setattr(class_name, req.property_name, value)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = niraapad_pb2.StaticSetterResp(exception=pickle.dumps(exception))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.StaticSetterTraceMsg(req=req,
                                                      resp=resp,
                                                      profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def Initialize(self, req, context):
        print("%s.__init__" % (req.backend_type), flush=True)

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

        start = default_timer()
        try:
            class_name = getattr(niraapad_backends_module, req.backend_type)
            self.backend_instances[req.backend_type][req.backend_instance_id] = \
                class_name(*args, **kwargs)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = niraapad_pb2.InitializeResp(exception=pickle.dumps(exception))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.InitializeTraceMsg(req=req,
                                                    resp=resp,
                                                    profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def Uninitialize(self, req, context):
        print("%s.__del__" % (req.backend_type), flush=True)

        exception = None

        backend_type = req.backend_type
        backend_instance_id = req.backend_instance_id

        start = default_timer()
        try:
            if backend_type in self.backend_instances:
                if backend_instance_id in self.backend_instances[backend_type]:
                    del self.backend_instances[backend_type][
                        backend_instance_id]

        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = niraapad_pb2.UninitializeResp(exception=pickle.dumps(exception))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.UninitializeTraceMsg(req=req,
                                                      resp=resp,
                                                      profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericMethod(self, req, context):
        print("%s.%s" % (req.backend_type, req.method_name), flush=True)

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

        start = default_timer()
        try:
            resp = getattr(
                self.backend_instances[req.backend_type][
                    req.backend_instance_id], req.method_name)(*args, **kwargs)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = niraapad_pb2.GenericMethodResp(exception=pickle.dumps(exception),
                                              resp=pickle.dumps(resp))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.GenericMethodTraceMsg(req=req,
                                                       resp=resp,
                                                       profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericGetter(self, req, context):
        print("%s.get_%s" % (req.backend_type, req.property_name), flush=True)

        # Getter functions are an extremely simplified version of GenericMethod
        # since they are interpreted not as functions but as variables, which
        # may be used in an expression; in this case, we simply return the
        # variable value.

        resp = None
        exception = None

        start = default_timer()
        try:
            resp = getattr(
                self.backend_instances[req.backend_type][
                    req.backend_instance_id], req.property_name)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = utils.sanitize_resp(req.property_name, resp)

        resp = niraapad_pb2.GenericGetterResp(exception=pickle.dumps(exception),
                                              resp=pickle.dumps(resp))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.GenericGetterTraceMsg(req=req,
                                                       resp=resp,
                                                       profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    def GenericSetter(self, req, context):
        print("%s.set_%s" % (req.backend_type, req.property_name), flush=True)

        # Setter functions are the opposite of getter functions. They simply
        # assign the provided value to the specified property.

        value = pickle.loads(req.value)

        resp = None
        exception = None

        start = default_timer()
        try:
            setattr(
                self.backend_instances[req.backend_type][
                    req.backend_instance_id], req.property_name, value)
        except Exception as e:
            NiraapadServicer.print_exception(e)
            exception = e
        end = default_timer()

        resp = niraapad_pb2.GenericSetterResp(exception=pickle.dumps(exception))

        profile = niraapad_pb2.CommandProfile(mo=int(utils.MO.VIA_MIDDLEBOX),
                                              exec_time_sec=(end - start))

        trace_msg = niraapad_pb2.GenericSetterTraceMsg(req=req,
                                                       resp=resp,
                                                       profile=profile)
        self.log_trace_msg(trace_msg)

        return resp

    @staticmethod
    def print_exception(e):
        print(">>>>>")
        print("Exception:")
        print(e)
        print("<<<<<", flush=True)


class NiraapadReplayServicer(niraapad_pb2_grpc.NiraapadServicer):
    """Provides methods that implement functionality of n9 replay server."""

    def __init__(self, tracedir):
        print("Initializing NiraapadReplayServicer", flush=True)
        self.tracedir = tracedir

    def sim_trace(self, id):
        try:
            start = default_timer()
            resp = self.trace_dict[id].resp
            while default_timer(
            ) - start < self.trace_dict[id].profile.exec_time_sec:
                continue
            return resp
        except Exception as e:
            print("Error: sim_trace failed with exception: %s" % e)
            exit(1)

    def LoadTrace(self, req, context):
        try:
            self.trace_dict = Tracer.get_trace_dict(
                os.path.join(self.tracedir, req.trace_file))
            return niraapad_pb2.LoadTraceResp(status=True)
        except Exception as e:
            print("Error: LoadTrace failed with exception: %s" % e)
            return niraapad_pb2.LoadTraceResp(status=False)

    def StaticMethod(self, req, context):
        print("%s.%s" % (req.backend_type, req.method_name), flush=True)
        return self.sim_trace(req.id)

    def StaticGetter(self, req, context):
        print("%s.get_%s" % (req.backend_type, req.property_name), flush=True)
        return self.sim_trace(req.id)

    def StaticSetter(self, req, context):
        print("%s.set_%s" % (req.backend_type, req.property_name), flush=True)
        return self.sim_trace(req.id)

    def Initialize(self, req, context):
        print("%s.__init__" % (req.backend_type), flush=True)
        return self.sim_trace(req.id)

    def Uninitialize(self, req, context):
        print("%s.__del__" % (req.backend_type), flush=True)
        return self.sim_trace(req.id)

    def GenericMethod(self, req, context):
        print("%s.%s" % (req.backend_type, req.method_name), flush=True)
        return self.sim_trace(req.id)

    def GenericGetter(self, req, context):
        print("%s.get_%s" % (req.backend_type, req.property_name), flush=True)
        return self.sim_trace(req.id)

    def GenericSetter(self, req, context):
        print("%s.get_%s" % (req.backend_type, req.property_name), flush=True)
        return self.sim_trace(req.id)

    def stop_tracing(self):
        pass


class NiraapadServer:

    def __init__(self, port, tracedir, keysdir=None, replay=False):
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
            server_credentials = grpc.ssl_server_credentials(
                ((private_key, certificate_chain),))
            self.server.add_secure_port('[::]:' + str(port), server_credentials)

        if replay == True:
            self.niraapad_servicer = NiraapadReplayServicer(tracedir=tracedir)
        else:
            self.niraapad_servicer = NiraapadServicer(tracedir=tracedir)

        niraapad_pb2_grpc.add_NiraapadServicer_to_server(
            self.niraapad_servicer, self.server)

    def start(self, wait=False):
        print("NiraapadServer::start", flush=True)
        self.server.start()

        # cleanly blocks the calling thread until the server terminates
        if wait:
            print("NiraapadServer::start waiting for termination", flush=True)
            self.server.wait_for_termination()

    def stop(self):
        print("NiraapadServer::stop", flush=True)
        self.niraapad_servicer.stop_tracing()
        event = self.server.stop(None)
        event.wait()

    def stop_tracing(self):
        self.niraapad_servicer.stop_tracing()

    def get_trace_file(self):
        return self.niraapad_servicer.tracer.trace_file
