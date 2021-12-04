import os
import grpc
import pickle
import importlib
import traceback
import threading

from timeit import default_timer
from datetime import datetime

import ratracer.protos.ratracer_pb2 as ratracer_pb2
import ratracer.protos.ratracer_pb2_grpc as ratracer_pb2_grpc
import ratracer.shared.utils as utils

ratracer_backends_module = importlib.import_module("ratracer.backends")


class RATracerClientHelper:
    """
    The RATracerClientHelper class encapsulates a gRPC client, which forwards
    all calls from class Serial on Lab Computer to the middlebox, which in turn
    is connected to the modules via actual serial communication. Unlike class
    Serial, there is only one global instance of class RATracerClientHelper.
    """

    def __init__(self, host, port, keysdir=None):
        if keysdir == None:
            print("RATracerClientHelper: Initialize an insecure GRPC channel")
            channel = grpc.insecure_channel(host + ':' + port)
        else:
            print("RATracerClientHelper: Initialize a secure GRPC channel")
            self.keysdir = keysdir
            server_crt_path = os.path.join(self.keysdir, "server.crt")
            with open(server_crt_path, 'rb') as f:
                trusted_certs = f.read()
            client_credentials = grpc.ssl_channel_credentials(
                root_certificates=trusted_certs)
            channel = grpc.secure_channel(host + ':' + port, client_credentials)

        self.stub = ratracer_pb2_grpc.RATracerStub(channel)
        self.backend_instance_count = 0

        print(
            "RATracerClientHelper: Send DeleteConnection RPC (for deleting old srever state)"
        )
        resp = self.stub.DeleteConnection(ratracer_pb2.DeleteConnectionReq())
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

        print("RATracerClientHelper: Send InitializeConnection RPC ")
        resp = self.stub.InitializeConnection(
            ratracer_pb2.InitializeConnectionReq())
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def __del__(self):
        resp = self.stub.DeleteConnection(ratracer_pb2.DeleteConnectionReq())
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def update_traces(self, trace_msg):
        if RATracerClient.ratracer_batch_traces:
            RATracerClient.ratracer_batched_trace_msgs.append(trace_msg)
            if default_timer(
            ) - RATracerClient.ratracer_batch_start_time > RATracerClient.ratracer_batch_duration_sec:
                self.stub.BatchedTrace(
                    ratracer_pb2.BatchedTraceMsg(trace_msgs=pickle.dumps(
                        RATracerClient.ratracer_batched_trace_msgs)))
                RATracerClient.ratracer_batch_start_time = default_timer()
                RATracerClient.ratracer_batched_trace_msg = []
        else:
            self.stub.BatchedTrace(
                ratracer_pb2.BatchedTraceMsg(
                    trace_msgs=pickle.dumps([trace_msg])))

    def static_method(self, id, backend_type, method_name, args_pickled,
                      kwargs_pickled):
        resp = self.stub.StaticMethod(
            ratracer_pb2.StaticMethodReq(
                id=id,
                backend_type=backend_type,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled,
                time_profiles=RATracerClient.get_time_profiles()))

        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def static_method_trace(self, id, backend_type, method_name, args_pickled,
                            kwargs_pickled, resp_pickled, exec_time_sec):
        trace_msg = ratracer_pb2.StaticMethodTraceMsg(
            req=ratracer_pb2.StaticMethodReq(
                id=id,
                backend_type=backend_type,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.StaticMethodResp(exception=pickle.dumps(None),
                                               resp=resp_pickled),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)

    def static_getter(self, id, backend_type, property_name):
        resp = self.stub.StaticGetter(
            ratracer_pb2.StaticGetterReq(
                id=id,
                backend_type=backend_type,
                property_name=property_name,
                time_profiles=RATracerClient.get_time_profiles()))

        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def static_getter_trace(self, id, backend_type, property_name, resp_pickled,
                            exec_time_sec):
        trace_msg = ratracer_pb2.StaticGetterTraceMsg(
            req=ratracer_pb2.StaticGetterReq(
                id=id,
                backend_type=backend_type,
                property_name=property_name,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.StaticGetterResp(exception=pickle.dumps(None),
                                               resp=resp_pickled),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)

    def static_setter(self, id, backend_type, property_name, value_pickled):
        resp = self.stub.StaticSetter(
            ratracer_pb2.StaticSetterReq(
                id=id,
                backend_type=backend_type,
                property_name=property_name,
                value=value_pickled,
                time_profiles=RATracerClient.get_time_profiles()))

        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def static_setter_trace(self, id, backend_type, property_name,
                            value_pickled, exec_time_sec):
        trace_msg = ratracer_pb2.StaticSetterTraceMsg(
            req=ratracer_pb2.StaticSetterReq(
                id=id,
                backend_type=backend_type,
                property_name=property_name,
                value=value_pickled,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.StaticSetterResp(exception=pickle.dumps(None)),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)

    def initialize(self, id, backend_type, args_pickled, kwargs_pickled,
                   stacktrace_pickled):
        self.backend_instance_count += 1
        resp = self.stub.Initialize(
            ratracer_pb2.InitializeReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=self.backend_instance_count,
                args=args_pickled,
                kwargs=kwargs_pickled,
                stacktrace=stacktrace_pickled,
                time_profiles=RATracerClient.get_time_profiles()))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return self.backend_instance_count

    def initialize_trace(self, id, backend_type, args_pickled, kwargs_pickled,
                         stacktrace_pickled, exec_time_sec):
        self.backend_instance_count += 1
        trace_msg = ratracer_pb2.InitializeTraceMsg(
            req=ratracer_pb2.InitializeReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=self.backend_instance_count,
                args=args_pickled,
                kwargs=kwargs_pickled,
                stacktrace=stacktrace_pickled,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.InitializeResp(exception=pickle.dumps(None)),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)
        return self.backend_instance_count

    def uninitialize(self, id, backend_type, backend_instance_id):
        resp = self.stub.Unintialize(
            ratracer_pb2.UnintializeReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                time_profiles=RATracerClient.get_time_profiles()))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def uninitialize_trace(self, id, backend_type, backend_instance_id,
                           exec_time_sec):
        trace_msg = ratracer_pb2.UnintializeTraceMsg(
            req=ratracer_pb2.UnintializeReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.GenericSetterResp(
                exception=pickle.dumps(None),
                profile=ratracer_pb2.CommandProfile(
                    mo=int(utils.MO.DIRECT_PLUS_MIDDLEBOX),
                    exec_time_sec=exec_time_sec)))
        self.update_traces(trace_msg)

    def generic_method(self, id, backend_type, backend_instance_id, method_name,
                       args_pickled, kwargs_pickled):
        resp = self.stub.GenericMethod(
            ratracer_pb2.GenericMethodReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled,
                time_profiles=RATracerClient.get_time_profiles()))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def generic_method_trace(self, id, backend_type, backend_instance_id,
                             method_name, args_pickled, kwargs_pickled,
                             resp_pickled, exec_time_sec):
        trace_msg = ratracer_pb2.GenericMethodTraceMsg(
            req=ratracer_pb2.GenericMethodReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.GenericMethodResp(exception=pickle.dumps(None),
                                                resp=resp_pickled),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)

    def generic_getter(self, id, backend_type, backend_instance_id,
                       property_name):
        resp = self.stub.GenericGetter(
            ratracer_pb2.GenericGetterReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name,
                time_profiles=RATracerClient.get_time_profiles()))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def generic_getter_trace(self, id, backend_type, backend_instance_id,
                             property_name, resp_pickled, exec_time_sec):
        trace_msg = ratracer_pb2.GenericGetterTraceMsg(
            req=ratracer_pb2.GenericGetterReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.GenericGetterResp(exception=pickle.dumps(None),
                                                resp=resp_pickled),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)

    def generic_setter(self, id, backend_type, backend_instance_id,
                       property_name, value_pickled):
        resp = self.stub.GenericSetter(
            ratracer_pb2.GenericSetterReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name,
                value=value_pickled,
                time_profiles=RATracerClient.get_time_profiles()))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def generic_setter_trace(self, id, backend_type, backend_instance_id,
                             property_name, value_pickled, exec_time_sec):
        trace_msg = ratracer_pb2.GenericSetterTraceMsg(
            req=ratracer_pb2.GenericSetterReq(
                id=id,
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name,
                value=value_pickled,
                time_profiles=RATracerClient.get_time_profiles()),
            resp=ratracer_pb2.GenericSetterResp(exception=pickle.dumps(None)),
            profile=ratracer_pb2.CommandProfile(mo=int(
                utils.MO.DIRECT_PLUS_MIDDLEBOX),
                                                exec_time_sec=exec_time_sec))
        self.update_traces(trace_msg)


class RATracerClient:
    # ratracer_mo = utils.MO.VIA_MIDDLEBOX
    ratracer_client_helper = None
    ratracer_mos = {}

    ratracer_lock = threading.Lock()
    ratracer_time_profiles = {}
    ratracer_req_id = 0

    ratracer_batch_traces = False
    ratracer_batch_duration_sec = 10
    ratracer_batch_start_time = default_timer()
    ratracer_batched_trace_msgs = []

    def __init__(self):
        if type(self) == SuperClass:
            raise Exception("RATracerClient must be subclassed.")

    def __del__(self):
        pass

    #def __new__(cls, *args, **kwargs):
    #    if cls == RATracerClient:
    #        raise TypeError("class RATracerClient must be subclassed.")
    #    return object.__new__(cls, *args, **kwargs)

    @staticmethod
    def update_arrival_time():
        RATracerClient.ratracer_lock.acquire()
        arrival_time = datetime.now().strftime("%Y:%m:%d:%H:%M:%S.%f")
        RATracerClient.ratracer_req_id += 1
        retval = [RATracerClient.ratracer_req_id, arrival_time]
        RATracerClient.ratracer_lock.release()
        return retval

    @staticmethod
    def update_departure_time(id, arrival_time):
        RATracerClient.ratracer_lock.acquire()
        departure_time = datetime.now().strftime("%Y:%m:%d:%H:%M:%S.%f")
        RATracerClient.ratracer_time_profiles[id] = [
            arrival_time, departure_time
        ]
        RATracerClient.ratracer_lock.release()
        return departure_time

    @staticmethod
    def get_time_profiles():
        RATracerClient.ratracer_lock.acquire()
        time_profiles = []
        for id, [arrival_time, departure_time
                ] in RATracerClient.ratracer_time_profiles.items():
            # print("TimeProfile: %d, %s, %s" % (id, arrival_time, departure_time))
            time_profiles.append(
                ratracer_pb2.TimeProfile(id=id,
                                         arrival_time=arrival_time,
                                         departure_time=departure_time))
        RATracerClient.ratracer_time_profiles = {}
        RATracerClient.ratracer_lock.release()
        return time_profiles

    @staticmethod
    def connect_to_middlebox(host, port, keysdir=None, debug=True):
        if debug:
            print("RATracerClient: Connect to middlebox at %s:%s" %
                  (host, port))
        try:
            if RATracerClient.ratracer_client_helper != None:
                del RATracerClient.ratracer_client_helper
            RATracerClient.ratracer_client_helper = RATracerClientHelper(
                host, port, keysdir)
            if debug:
                print("RATracerClient: Middlebox successfully connected")
        except Exception as e:
            RATracerClient.handle_any_exception("RATracerClient",
                                                "connect_to_middlebox", e)
            if debug:
                print(
                    "EXITING. Please try again. If error persists, please try without RATracer."
                )
            exit()

        for backend in utils.BACKENDS:
            RATracerClient.ratracer_mos[backend] = utils.MO.VIA_MIDDLEBOX
            if debug:
                print("RATracerClient: Initial mode of operation",
                      utils.MO.VIA_MIDDLEBOX,
                      flush=True)

    @staticmethod
    def update_mos(default_mo=utils.MO.VIA_MIDDLEBOX,
                   exceptions={},
                   debug=True):
        if debug:
            print("RATracerClient: Updating mode of operation")
        for backend in utils.BACKENDS:
            RATracerClient.ratracer_mos[backend] = default_mo
        for backend, mo in exceptions.items():
            assert (backend in utils.BACKENDS)
            assert (mo in utils.MO)
            RATracerClient.ratracer_mos[backend] = mo
            RATracerClient.update_group_mos(backend, mo)
        for backend, mo in RATracerClient.ratracer_mos.items():
            if debug:
                print("  RATracerClinet: %s --> %s" % (backend, mo))

    @staticmethod
    def update_group_mos(backend, mo):
        for key, group in utils.backend_groups.items():
            if backend not in group:
                continue
            for member in group:
                assert (member in utils.BACKENDS)
                RATracerClient.ratracer_mos[member] = mo

    @staticmethod
    def static_method(backend_type, *args, **kwargs):
        [id, arrival_time] = RATracerClient.update_arrival_time()
        method_name = utils.CALLER_METHOD_NAME()
        class_name = getattr(ratracer_backends_module, backend_type)
        resp = None

        if RATracerClient.ratracer_mos[backend_type] == utils.MO.DIRECT:
            resp = getattr(class_name, method_name)(*args, **kwargs)

        elif RATracerClient.ratracer_mos[
                backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                resp = RATracerClient.ratracer_client_helper.static_method(
                    id, backend_type, method_name, pickle.dumps(args),
                    pickle.dumps(kwargs))
            except Exception as e:
                RATracerClient.handle_any_exception(backend_type, method_name,
                                                    e, True)
                assert (False)

        elif RATracerClient.ratracer_mos[
                backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            start = default_timer()
            resp = getattr(class_name, method_name)(*args, **kwargs)
            end = default_timer()

            try:
                trace_resp = utils.sanitize_resp(method_name, resp)
                RATracerClient.ratracer_client_helper.static_method_trace(
                    arrival_time, backend_type, method_name, pickle.dumps(args),
                    pickle.dumps(kwargs), pickle.dumps(trace_resp),
                    (end - start))
            except Exception as e:
                RATracerClient.handle_any_exception(backend_type,
                                                    "%s_trace" % method_name, e)

        RATracerClient.update_departure_time(id, arrival_time)
        return resp

    @staticmethod
    def static_getter(backend_type, property_name):
        [id, arrival_time] = RATracerClient.update_arrival_time()
        class_name = getattr(ratracer_backends_module, backend_type)
        resp = None

        if RATracerClient.ratracer_mos[backend_type] == utils.MO.DIRECT:
            resp = getattr(class_name, property_name)

        elif RATracerClient.ratracer_mos[
                backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                resp = RATracerClient.ratracer_client_helper.static_getter(
                    id, backend_type, property_name)
            except Exception as e:
                RATracerClient.handle_any_exception(
                    backend_type, "get_%s_trace" % property_name, e, True)

        elif RATracerClient.ratracer_mos[
                backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            start = default_timer()
            resp = getattr(class_name, property_name)
            end = default_timer()

            try:
                RATracerClient.ratracer_client_helper.static_getter_trace(
                    id, backend_type, property_name, pickle.dumps(resp),
                    (end - start))
            except Exception as e:
                RATracerClient.handle_any_exception(
                    backend_type, "get_%s_trace" % property_name, e)

        RATracerClient.update_departure_time(id, arrival_time)
        return resp

    @staticmethod
    def static_setter(backend_type, property_name, value):
        [id, arrival_time] = RATracerClient.update_arrival_time()
        class_name = getattr(ratracer_backends_module, backend_type)

        if RATracerClient.ratracer_mos[backend_type] == utils.MO.DIRECT:
            setattr(class_name, property_name, value)

        elif RATracerClient.ratracer_mos[
                backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                RATracerClient.ratracer_client_helper.static_setter(
                    id, backend_type, property_name, pickle.dumps(value))
            except Exception as e:
                RATracerClient.handle_any_exception(backend_type,
                                                    "set_%s" % property_name, e,
                                                    True)

        elif RATracerClient.ratracer_mos[
                backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            start = default_timer()
            setattr(class_name, property_name, value)
            end = default_timer()

            try:
                RATracerClient.ratracer_client_helper.static_setter_trace(
                    id, backend_type, property_name, pickle.dumps(value),
                    (end - start))
            except Exception as e:
                RATracerClient.handle_any_exception(
                    backend_type, "set_%s_trace" % property_name, e)

        RATracerClient.update_departure_time(id, arrival_time)

    def initialize(self, *args, **kwargs):
        """
        Since the __init__ function is invoked similar to static methods,
        that is, it is invoked using the class name, this function is
        analogous to the static_method function above, except that we do not
        need a variable for the method name, which is known to be "__init__"
        in this case.
        """
        [id, arrival_time] = RATracerClient.update_arrival_time()
        stacktrace = traceback.extract_stack()
        class_name = getattr(ratracer_backends_module,
                             self.ratracer_backend_type)

        if RATracerClient.ratracer_mos[self.ratracer_backend_type] == utils.MO.DIRECT or \
           RATracerClient.ratracer_mos[self.ratracer_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            start = default_timer()
            self.ratracer_backend_instance = class_name(*args, **kwargs)
            end = default_timer()

        if RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                self.ratracer_backend_instance_id = \
                    RATracerClient.ratracer_client_helper.initialize(
                        id, self.ratracer_backend_type, pickle.dumps(args),
                        pickle.dumps(kwargs), pickle.dumps(stacktrace))
            except Exception as e:
                self.ratracer_backend_instance_id = 0
                self.handle_exception("initialize", e, True)

        if RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            try:
                self.ratracer_backend_instance_id = \
                    RATracerClient.ratracer_client_helper.initialize_trace(
                        id, self.ratracer_backend_type, pickle.dumps(args),
                        pickle.dumps(kwargs), pickle.dumps(stacktrace), (end - start))
            except Exception as e:
                self.ratracer_backend_instance_id = 0
                self.handle_exception("initialize_trace", e)

        RATracerClient.update_departure_time(id, arrival_time)

    def uninitialize(self, *args, **kwargs):
        """
        For the __del__ method, the method is invoked using
        the class instance name and not directly using the class name.
        Thus, the following set of statements is analogous to the function
        definition of the static_methods function above, except that we deal
        with specific class instances identified using their unique
        identifiers ("ratracer_backend_instance_id"), which were set during
        initialization.
        """
        [id, arrival_time] = RATracerClient.update_arrival_time()

        if RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT:
            del self.ratracer_backend_instance

        elif self.ratracer_backend_instance_id == 0:
            pass

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                RATracerClient.ratracer_client_helper.uninitialize(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id)
            except Exception as e:
                self.handle_exception("uninitialize", e, True)

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:

            start = default_timer()
            del self.ratracer_backend_instance
            end = default_timer()

            try:
                RATracerClient.ratracer_client_helper.unintialize_trace(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, (end - start))
            except Exception as e:
                self.handle_exception("unintialize_trace" % e)

        RATracerClient.update_departure_time(id, arrival_time)

    def generic_method(self, *args, **kwargs):
        """
        For any generic class instance method, the logic is similar to that
        of any generic static method, except that the method is invoked using
        the class instance name and not directly using the class name.
        Thus, the following set of statements is analogous to the function
        definition of the static_methods function above, except that we deal
        with specific class instances identified using their unique
        identifiers ("ratracer_backend_instance_id"), which were set during
        initialization.
        """
        [id, arrival_time] = RATracerClient.update_arrival_time()
        method_name = utils.CALLER_METHOD_NAME()
        resp = None

        if RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT:
            resp = getattr(self.ratracer_backend_instance,
                           method_name)(*args, **kwargs)

        elif self.ratracer_backend_instance_id == 0:
            pass

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                resp = RATracerClient.ratracer_client_helper.generic_method(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, method_name,
                    pickle.dumps(args), pickle.dumps(kwargs))
            except Exception as e:
                self.handle_exception(method_name, e, True)

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:

            start = default_timer()
            resp = getattr(self.ratracer_backend_instance,
                           method_name)(*args, **kwargs)
            end = default_timer()

            try:
                RATracerClient.ratracer_client_helper.generic_method_trace(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, method_name,
                    pickle.dumps(args), pickle.dumps(kwargs),
                    pickle.dumps(resp), (end - start))
            except Exception as e:
                self.handle_exception("%s_trace" % method_name, e)

        RATracerClient.update_departure_time(id, arrival_time)
        return resp

    def generic_getter(self, property_name):
        """
        Getter functions are an extremely simplified version of GenericMethod
        since they are interpreted not as functions but as variables, which
        may be used in an expression; in this case, we simply return the
        variable value.
        """
        [id, arrival_time] = RATracerClient.update_arrival_time()
        resp = None

        if RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT:
            resp = getattr(self.ratracer_backend_instance, property_name)

        elif self.ratracer_backend_instance_id == 0:
            pass

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                resp = RATracerClient.ratracer_client_helper.generic_getter(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, property_name)
            except Exception as e:
                self.handle_exception("get_%s" % property_name, e, True)

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:

            start = default_timer()
            resp = getattr(self.ratracer_backend_instance, property_name)
            end = default_timer()

            try:
                RATracerClient.ratracer_client_helper.generic_getter_trace(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, property_name,
                    pickle.dumps(resp), (end - start))
            except Exception as e:
                self.handle_exception("get_%s_trace" % property_name, e)

        RATracerClient.update_departure_time(id, arrival_time)
        return resp

    def generic_setter(self, property_name, value):
        """
        Setter functions are the opposite of getter functions. They simply
        assign the provided value to the specified property.
        """
        [id, arrival_time] = RATracerClient.update_arrival_time()

        if RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT:
            setattr(self.ratracer_backend_instance, property_name, value)

        elif self.ratracer_backend_instance_id == 0:
            pass

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                RATracerClient.ratracer_client_helper.generic_setter(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, property_name,
                    pickle.dumps(value))
            except Exception as e:
                self.handle_exception("set_%s" % property_name, e, True)

        elif RATracerClient.ratracer_mos[
                self.ratracer_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            start = default_timer()
            setattr(self.ratracer_backend_instance, property_name, value)
            end = default_timer()

            try:
                RATracerClient.ratracer_client_helper.generic_setter_trace(
                    id, self.ratracer_backend_type,
                    self.ratracer_backend_instance_id, property_name,
                    pickle.dumps(value), (end - start))
            except Exception as e:
                self.handle_exception("set_%s_trace" % property_name, e)

        RATracerClient.update_departure_time(id, arrival_time)

    def __getattribute__(self, key):
        """
        This function overrides the object.__getattribute__ method and is used
        trap and appropriately handle all read accesses to instance variables.
        """

        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return self.generic_getter(key)

    def __setattr__(self, key, value):
        """
        This function overrides the object.__setattr__ method and is used to
        trap and appropriately handle all write accesses to instance variables.
        We distinguish between HeinLab-specific variables and
        RATracer-speicific variables using the "ratracer" prefix. Tihs
        distinction is necessary when assigning values or seting new
        variables. For HeinLab-specific variables, we need to assign the
        corresponding variables in the original class, e.g., DirectSerial,
        which may be on the remote machine as well, depending on the mode of
        operation. However, for RATracer-specific variables, we need to
        assign the variables in this class (RATracerCLient) itself!
        """

        if key.startswith("ratracer"):
            return object.__setattr__(self, key, value)

        self.generic_setter(key, value)

    def handle_exception(self, function_name, exception, raise_exception=False):
        RATracerClient.handle_any_exception(self.ratracer_backend_type,
                                            function_name, exception,
                                            raise_exception)

    @staticmethod
    def handle_any_exception(backend_type,
                             function_name,
                             exception,
                             raise_exception=False):
        print(">>>>>")
        print("Call to middlebox (%s.%s) failed with exception:" %
              (backend_type, function_name))
        print(exception)
        print("<<<<<", flush=True)
        if raise_exception:
            raise exception
