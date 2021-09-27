import os
import grpc
import pickle
import importlib
import traceback

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc
import niraapad.shared.utils as utils

niraapad_backends_module = importlib.import_module("niraapad.backends")


class NiraapadClientHelper:
    """
    The NiraapadClientHelper class encapsulates a gRPC client, which forwards
    all calls from class Serial on Lab Computer to the middlebox, which in turn
    is connected to the modules via actual serial communication. Unlike class
    Serial, there is only one global instance of class NiraapadClientHelper.
    """

    def __init__(self, host, port, keysdir=None):
        if keysdir == None:
            print("NiraapadClientHelper: Initialize an insecure GRPC channel")
            channel = grpc.insecure_channel(host + ':' + port)
        else:
            print("NiraapadClientHelper: Initialize a secure GRPC channel")
            self.keysdir = keysdir
            server_crt_path = os.path.join(self.keysdir, "server.crt")
            with open(server_crt_path, 'rb') as f:
                trusted_certs = f.read()
            client_credentials = grpc.ssl_channel_credentials(
                root_certificates=trusted_certs)
            channel = grpc.secure_channel(host + ':' + port, client_credentials)

        self.stub = niraapad_pb2_grpc.NiraapadStub(channel)
        self.backend_instance_count = 0

        print(
            "NiraapadClientHelper: Send DeleteConnection RPC (for deleting old srever state)"
        )
        resp = self.stub.DeleteConnection(niraapad_pb2.DeleteConnectionReq())
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

        print("NiraapadClientHelper: Send InitializeConnection RPC ")
        resp = self.stub.InitializeConnection(
            niraapad_pb2.InitializeConnectionReq())
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def __del__(self):
        resp = self.stub.DeleteConnection(niraapad_pb2.DeleteConnectionReq())
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def static_method(self, backend_type, method_name, args_pickled,
                      kwargs_pickled):
        resp = self.stub.StaticMethod(
            niraapad_pb2.StaticMethodReq(backend_type=backend_type,
                                         method_name=method_name,
                                         args=args_pickled,
                                         kwargs=kwargs_pickled))

        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def static_method_trace(self, backend_type, method_name, args_pickled,
                            kwargs_pickled, resp_pickled):
        self.stub.StaticMethodTrace(
            niraapad_pb2.StaticMethodTraceMsg(
                req=niraapad_pb2.StaticMethodReq(backend_type=backend_type,
                                                 method_name=method_name,
                                                 args=args_pickled,
                                                 kwargs=kwargs_pickled),
                resp=niraapad_pb2.StaticMethodResp(exception=pickle.dumps(None),
                                                   resp=resp_pickled)))

    def static_getter(self, backend_type, property_name):
        resp = self.stub.StaticGetter(
            niraapad_pb2.StaticGetterReq(backend_type=backend_type,
                                         property_name=property_name))

        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def static_getter_trace(self, backend_type, property_name, resp_pickled):
        resp = self.stub.StaticGetterTrace(
            niraapad_pb2.StaticGetterTraceMsg(
                req=niraapad_pb2.StaticGetterReq(backend_type=backend_type,
                                                 property_name=property_name),
                resp=niraapad_pb2.StaticGetterResp(exception=pickle.dumps(None),
                                                   resp=resp_pickled)))

    def static_setter(self, backend_type, property_name, value_pickled):
        resp = self.stub.StaticSetter(
            niraapad_pb2.StaticSetterReq(backend_type=backend_type,
                                         property_name=property_name,
                                         value=value_pickled))

        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def static_setter_trace(self, backend_type, property_name, value_pickled):
        self.stub.StaticSetterTrace(
            niraapad_pb2.StaticSetterTraceMsg(
                req=niraapad_pb2.StaticSetterReq(backend_type=backend_type,
                                                 property_name=property_name,
                                                 value=value_pickled),
                resp=niraapad_pb2.StaticSetterResp(
                    exception=pickle.dumps(None))))

    def initialize(self, backend_type, args_pickled, kwargs_pickled,
                   stacktrace_pickled):
        self.backend_instance_count += 1
        resp = self.stub.Initialize(
            niraapad_pb2.InitializeReq(
                backend_type=backend_type,
                backend_instance_id=self.backend_instance_count,
                args=args_pickled,
                kwargs=kwargs_pickled,
                stacktrace=stacktrace_pickled))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return self.backend_instance_count

    def initialize_trace(self, backend_type, args_pickled, kwargs_pickled,
                         stacktrace_pickled):
        self.backend_instance_count += 1
        self.stub.InitializeTrace(
            niraapad_pb2.InitializeTraceMsg(
                req=niraapad_pb2.InitializeReq(
                    backend_type=backend_type,
                    backend_instance_id=self.backend_instance_count,
                    args=args_pickled,
                    kwargs=kwargs_pickled,
                    stacktrace=stacktrace_pickled),
                resp=niraapad_pb2.InitializeResp(exception=pickle.dumps(None))))
        return self.backend_instance_count

    def generic_method(self, backend_type, backend_instance_id, method_name,
                       args_pickled, kwargs_pickled):
        resp = self.stub.GenericMethod(
            niraapad_pb2.GenericMethodReq(
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def generic_method_trace(self, backend_type, backend_instance_id,
                             method_name, args_pickled, kwargs_pickled,
                             resp_pickled):
        self.stub.GenericMethodTrace(
            niraapad_pb2.GenericMethodTraceMsg(
                req=niraapad_pb2.GenericMethodReq(
                    backend_type=backend_type,
                    backend_instance_id=backend_instance_id,
                    method_name=method_name,
                    args=args_pickled,
                    kwargs=kwargs_pickled),
                resp=niraapad_pb2.GenericMethodResp(
                    exception=pickle.dumps(None), resp=resp_pickled)))

    def generic_getter(self, backend_type, backend_instance_id, property_name):
        resp = self.stub.GenericGetter(
            niraapad_pb2.GenericGetterReq(
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception
        return pickle.loads(resp.resp)

    def generic_getter_trace(self, backend_type, backend_instance_id,
                             property_name, resp_pickled):
        self.stub.GenericGetterTrace(
            niraapad_pb2.GenericGetterTraceMsg(
                req=niraapad_pb2.GenericGetterReq(
                    backend_type=backend_type,
                    backend_instance_id=backend_instance_id,
                    property_name=property_name),
                resp=niraapad_pb2.GenericGetterResp(
                    exception=pickle.dumps(None), resp=resp_pickled)))

    def generic_setter(self, backend_type, backend_instance_id, property_name,
                       value_pickled):
        resp = self.stub.GenericSetter(
            niraapad_pb2.GenericSetterReq(
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name,
                value=value_pickled))
        exception = pickle.loads(resp.exception)
        if exception != None:
            raise exception

    def generic_setter_trace(self, backend_type, backend_instance_id,
                             property_name, value_pickled):
        self.stub.GenericSetterTrace(
            niraapad_pb2.GenericSetterTraceMsg(
                req=niraapad_pb2.GenericSetterReq(
                    backend_type=backend_type,
                    backend_instance_id=backend_instance_id,
                    property_name=property_name,
                    value=value_pickled),
                resp=niraapad_pb2.GenericSetterResp(
                    exception=pickle.dumps(None))))


class NiraapadClient:
    # niraapad_mo = utils.MO.VIA_MIDDLEBOX
    niraapad_client_helper = None
    niraapad_mos = {}

    def __init__(self):
        if type(self) == SuperClass:
            raise Exception("NiraapadClient must be subclassed.")

    #def __new__(cls, *args, **kwargs):
    #    if cls == NiraapadClient:
    #        raise TypeError("class NiraapadClient must be subclassed.")
    #    return object.__new__(cls, *args, **kwargs)

    @staticmethod
    def connect_to_middlebox(host, port, keysdir=None):
        print("NiraapadClient: Connect to middlebox at %s:%s" % (host, port))
        try:
            if NiraapadClient.niraapad_client_helper != None:
                del NiraapadClient.niraapad_client_helper
            NiraapadClient.niraapad_client_helper = NiraapadClientHelper(
                host, port, keysdir)
            print("NiraapadClient: Middlebox successfully connected")
        except Exception as e:
            NiraapadClient.handle_any_exception("NiraapadClient",
                                                "connect_to_middlebox", e)
            print(
                "EXITING. Please try again. If error persists, please try without Niraapad."
            )
            exit()

        for backend in utils.BACKENDS:
            NiraapadClient.niraapad_mos[backend] = utils.MO.VIA_MIDDLEBOX
            print("NiraapadClient: Initial mode of operation",
                  utils.MO.VIA_MIDDLEBOX,
                  flush=True)

    @staticmethod
    def update_mos(default_mo=utils.MO.VIA_MIDDLEBOX, exceptions={}):
        print("NiraapadClient: Updating mode of operation")
        for backend in utils.BACKENDS:
            NiraapadClient.niraapad_mos[backend] = default_mo
        for backend, mo in exceptions.items():
            # print("NiraapadClient: EXCEPTION: %s --> %s" % (backend, mo))
            assert (backend in utils.BACKENDS)
            assert (mo in utils.MO)
            NiraapadClient.niraapad_mos[backend] = mo
            NiraapadClient.update_group_mos(backend, mo)
        for backend, mo in NiraapadClient.niraapad_mos.items():
            print("  NiraapadClinet: %s --> %s" % (backend, mo))

    @staticmethod
    def update_group_mos(backend, mo):
        for key, group in utils.backend_groups.items():
            if backend not in group:
                continue
            for member in group:
                assert (member in utils.BACKENDS)
                NiraapadClient.niraapad_mos[member] = mo

    @staticmethod
    def static_method(backend_type, *args, **kwargs):
        method_name = utils.CALLER_METHOD_NAME()

        class_name = getattr(niraapad_backends_module, backend_type)

        if NiraapadClient.niraapad_mos[backend_type] == utils.MO.DIRECT:
            return getattr(class_name, method_name)(*args, **kwargs)

        if NiraapadClient.niraapad_mos[backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                return NiraapadClient.niraapad_client_helper.static_method(
                    backend_type, method_name, pickle.dumps(args),
                    pickle.dumps(kwargs))
            except Exception as e:
                NiraapadClient.handle_any_exception(backend_type, method_name,
                                                    e, True)

        resp = getattr(class_name, method_name)(*args, **kwargs)

        try:
            trace_resp = utils.sanitize_resp(method_name, resp)
            NiraapadClient.niraapad_client_helper.static_method_trace(
                backend_type, method_name, pickle.dumps(args),
                pickle.dumps(kwargs), pickle.dumps(trace_resp))
        except Exception as e:
            NiraapadClient.handle_any_exception(backend_type,
                                                "%s_trace" % method_name, e)

        return resp

    @staticmethod
    def static_getter(backend_type, property_name):
        class_name = getattr(niraapad_backends_module, backend_type)

        print("backend_type", backend_type, flush=True)
        if NiraapadClient.niraapad_mos[backend_type] == utils.MO.DIRECT:
            return getattr(class_name, property_name)

        if NiraapadClient.niraapad_mos[backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                return NiraapadClient.niraapad_client_helper.static_getter(
                    backend_type, property_name)
            except Exception as e:
                NiraapadClient.handle_any_exception(
                    backend_type, "get_%s_trace" % property_name, e, True)

        resp = getattr(class_name, property_name)

        try:
            NiraapadClient.niraapad_client_helper.static_getter_trace(
                backend_type, property_name, pickle.dumps(resp))
        except Exception as e:
            NiraapadClient.handle_any_exception(backend_type,
                                                "get_%s_trace" % property_name,
                                                e)

        return resp

    @staticmethod
    def static_setter(backend_type, property_name, value):
        class_name = getattr(niraapad_backends_module, backend_type)

        if NiraapadClient.niraapad_mos[backend_type] == utils.MO.DIRECT:
            return setattr(class_name, property_name, value)

        if NiraapadClient.niraapad_mos[backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                return NiraapadClient.niraapad_client_helper.static_setter(
                    backend_type, property_name, pickle.dumps(value))
            except Exception as e:
                NiraapadClient.handle_any_exception(backend_type,
                                                    "set_%s" % property_name, e,
                                                    True)

        setattr(class_name, property_name, value)

        try:
            NiraapadClient.niraapad_client_helper.static_setter_trace(
                backend_type, property_name, pickle.dumps(value))
        except Exception as e:
            NiraapadClient.handle_any_exception(backend_type,
                                                "set_%s_trace" % property_name,
                                                e)

    def initialize(self, *args, **kwargs):
        """
        Since the __init__ function is invoked similar to static methods,
        that is, it is invoked using the class name, this function is
        analogous to the static_method function above, except that we do not
        need a variable for the method name, which is known to be "__init__"
        in this case.
        """
        stacktrace = traceback.extract_stack()

        class_name = getattr(niraapad_backends_module,
                             self.niraapad_backend_type)

        if NiraapadClient.niraapad_mos[self.niraapad_backend_type] == utils.MO.DIRECT or \
           NiraapadClient.niraapad_mos[self.niraapad_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            self.niraapad_backend_instance = class_name(*args, **kwargs)

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                self.niraapad_backend_instance_id = \
                    NiraapadClient.niraapad_client_helper.initialize(
                        self.niraapad_backend_type, pickle.dumps(args),
                        pickle.dumps(kwargs), pickle.dumps(stacktrace))
            except Exception as e:
                self.niraapad_backend_instance_id = 0
                self.handle_exception("initialize", e, True)

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            try:
                self.niraapad_backend_instance_id = \
                    NiraapadClient.niraapad_client_helper.initialize_trace(
                        self.niraapad_backend_type, pickle.dumps(args),
                        pickle.dumps(kwargs), pickle.dumps(stacktrace))
            except Exception as e:
                self.niraapad_backend_instance_id = 0
                self.handle_exception("initialize_trace", e)

    def generic_method(self, *args, **kwargs):
        """
        For any generic class instance method, the logic is similar to that
        of any generic static method, except that the method is invoked using
        the class instance name and not directly using the class name.
        Thus, the following set of statements is analogous to the function
        definition of the static_methods function above, except that we deal
        with specific class instances identified using their unique
        identifiers ("niraapad_backend_instance_id"), which were set during
        initialization.
        """
        method_name = utils.CALLER_METHOD_NAME()

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.DIRECT:
            return getattr(self.niraapad_backend_instance,
                           method_name)(*args, **kwargs)

        if self.niraapad_backend_instance_id == 0:
            return

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                return NiraapadClient.niraapad_client_helper.generic_method(
                    self.niraapad_backend_type,
                    self.niraapad_backend_instance_id, method_name,
                    pickle.dumps(args), pickle.dumps(kwargs))
            except Exception as e:
                self.handle_exception(method_name, e, True)

        resp = getattr(self.niraapad_backend_instance, method_name)(*args,
                                                                    **kwargs)

        try:
            NiraapadClient.niraapad_client_helper.generic_method_trace(
                self.niraapad_backend_type, self.niraapad_backend_instance_id,
                method_name, pickle.dumps(args), pickle.dumps(kwargs),
                pickle.dumps(resp))
        except Exception as e:
            self.handle_exception("%s_trace" % method_name, e)

        return resp

    def generic_getter(self, property_name):
        """
        Getter functions are an extremely simplified version of GenericMethod
        since they are interpreted not as functions but as variables, which
        may be used in an expression; in this case, we simply return the
        variable value.
        """

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.DIRECT:
            return getattr(self.niraapad_backend_instance, property_name)

        if self.niraapad_backend_instance_id == 0:
            return

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                return NiraapadClient.niraapad_client_helper.generic_getter(
                    self.niraapad_backend_type,
                    self.niraapad_backend_instance_id, property_name)
            except Exception as e:
                self.handle_exception("get_%s" % property_name, e, True)

        resp = getattr(self.niraapad_backend_instance, property_name)

        try:
            NiraapadClient.niraapad_client_helper.generic_getter_trace(
                self.niraapad_backend_type, self.niraapad_backend_instance_id,
                property_name, pickle.dumps(resp))
        except Exception as e:
            self.handle_exception("get_%s_trace" % property_name, e)

        return resp

    def generic_setter(self, property_name, value):
        """
        Setter functions are the opposite of getter functions. They simply
        assign the provided value to the specified property.
        """

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.DIRECT:
            setattr(self.niraapad_backend_instance, property_name, value)
            return

        if self.niraapad_backend_instance_id == 0:
            return

        if NiraapadClient.niraapad_mos[
                self.niraapad_backend_type] == utils.MO.VIA_MIDDLEBOX:
            try:
                NiraapadClient.niraapad_client_helper.generic_setter(
                    self.niraapad_backend_type,
                    self.niraapad_backend_instance_id, property_name,
                    pickle.dumps(value))
                return
            except Exception as e:
                self.handle_exception("set_%s" % property_name, e, True)

        setattr(self.niraapad_backend_instance, property_name, value)

        try:
            NiraapadClient.niraapad_client_helper.generic_setter_trace(
                self.niraapad_backend_type, self.niraapad_backend_instance_id,
                property_name, pickle.dumps(value))
        except Exception as e:
            self.handle_exception("set_%s_trace" % property_name, e)

        return

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
        Niraapad-speicific variables using the "niraapad" prefix. Tihs
        distinction is necessary when assigning values or seting new
        variables. For HeinLab-specific variables, we need to assign the
        corresponding variables in the original class, e.g., DirectSerial,
        which may be on the remote machine as well, depending on the mode of
        operation. However, for Niraapad-specific variables, we need to
        assign the variables in this class (NiraapadCLient) itself!
        """

        if key.startswith("niraapad"):
            return object.__setattr__(self, key, value)

        self.generic_setter(key, value)

    def handle_exception(self, function_name, exception, raise_exception=False):
        NiraapadClient.handle_any_exception(self.niraapad_backend_type,
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
