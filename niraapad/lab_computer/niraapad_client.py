import os
import grpc
import pickle
import importlib

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc
import niraapad.shared.utils as utils

class NiraapadClientHelper:
    """
    The NiraapadClientHelper class encapsulates a gRPC client, which forwards all
    calls from class Serial on Lab Computer to the middlebox, which in turn is
    connected to the modules via actual serial communication. Unlike class
    Serial, there is only one global instance of class NiraapadClientHelper.
    """

    def __init__(self, host, port, keysdir):
        self.keysdir = keysdir
        server_crt_path = os.path.join(self.keysdir, "server.crt")

        with open(server_crt_path, 'rb') as f:
            trusted_certs = f.read()
        client_credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs)
        channel = grpc.secure_channel(host + ':' + port, client_credentials)
        self.stub = niraapad_pb2_grpc.NiraapadStub(channel)

        self.backend_instance_count = 0

    def static_method(self, backend_type, method_name, args_pickled,
                      kwargs_pickled):
        resp = self.stub.StaticMethod(niraapad_pb2.StaticMethodReq(
            backend_type=backend_type, method_name=method_name,
            args=args_pickled, kwargs=kwargs_pickled))

        exception = pickle.loads(resp.exception)
        if exception != None: raise exception
        return pickle.loads(resp.resp)

    def static_method_trace(self, backend_type, method_name, args_pickled,
                            kwargs_pickled, resp_pickled):
        self.stub.StaticMethodTrace(niraapad_pb2.StaticMethodTraceMsg(
            req=niraapad_pb2.StaticMethodReq(
                backend_type=backend_type, method_name=method_name,
                args=args_pickled, kwargs=kwargs_pickled),
            resp=niraapad_pb2.StaticMethodResp(resp=resp_pickled)))

    def initialize(self, backend_type, args_pickled, kwargs_pickled):
        self.backend_instance_count += 1
        resp = self.stub.Initialize(niraapad_pb2.InitializeReq(
            backend_type=backend_type,
            backend_instance_id=self.backend_instance_count,
            args=args_pickled,
            kwargs=kwargs_pickled))
        exception = pickle.loads(resp.exception)
        if exception != None: raise exception
        return self.backend_instance_count

    def initialize_trace(self, backend_type, args_pickled, kwargs_pickled):
        self.backend_instance_count += 1
        self.stub.InitializeTrace(niraapad_pb2.InitializeTraceMsg(
            req=niraapad_pb2.InitializeReq(
                backend_type=backend_type,
                backend_instance_id=self.backend_instance_count,
                args=args_pickled,
                kwargs=kwargs_pickled),
            resp=niraapad_pb2.InitializeResp(
                exception=pickle.dumps(None))))
        return self.backend_instance_count

    def generic_method(self, backend_type, backend_instance_id, method_name,
                       args_pickled, kwargs_pickled):
        resp = self.stub.GenericMethod(niraapad_pb2.GenericMethodReq(
            backend_type=backend_type, backend_instance_id=backend_instance_id,
            method_name=method_name, args=args_pickled, kwargs=kwargs_pickled))
        exception = pickle.loads(resp.exception)
        if exception != None: raise exception
        return pickle.loads(resp.resp)

    def generic_method_trace(self, backend_type, backend_instance_id,
                             method_name, args_pickled, kwargs_pickled,
                             resp_pickled):
        self.stub.GenericMethodTrace(niraapad_pb2.GenericMethodTraceMsg(
            req=niraapad_pb2.GenericMethodReq(
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled),
            resp=niraapad_pb2.GenericMethodResp(resp=resp_pickled)))

    def generic_getter(self, backend_type, backend_instance_id, property_name):
        resp = self.stub.GenericGetter(niraapad_pb2.GenericGetterReq(
            backend_type=backend_type,
            backend_instance_id=backend_instance_id,
            property_name=property_name))
        exception = pickle.loads(resp.exception)
        if exception != None: raise exception
        return pickle.loads(resp.resp)

    def generic_getter_trace(self, backend_type, backend_instance_id,
                             property_name, resp_pickled):
        self.stub.GenericGetterTrace(niraapad_pb2.GenericGetterTraceMsg(
            req=niraapad_pb2.GenericGetterReq(
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name),
            resp=niraapad_pb2.GenericGetterResp(resp=resp_pickled)))

    def generic_setter(self, backend_type, backend_instance_id, property_name,
                       value_pickled):
        resp = self.stub.GenericSetter(niraapad_pb2.GenericSetterReq(
            backend_type=backend_type, backend_instance_id=backend_instance_id,
            property_name=property_name, value=value_pickled))
        exception = pickle.loads(resp.exception)
        if exception != None: raise exception

    def generic_setter_trace(self, backend_type, backend_instance_id,
                             property_name, value_pickled):
        self.stub.GenericSetterTrace(niraapad_pb2.GenericSetterTraceMsg(
            req=niraapad_pb2.GenericSetterReq(
                backend_type=backend_type,
                backend_instance_id=backend_instance_id,
                property_name=property_name,
                value=value_pickled),
            resp=niraapad_pb2.GenericSetterResp(
                exception=pickle.dumps(None))))

class NiraapadClient:
    mo = utils.MO.VIA_MIDDLEBOX
    niraapad_client_helper = None

    def __init__(self):
        if type(self) == SuperClass:
            raise Exception("NiraapadClient must be subclassed.")

    #def __new__(cls, *args, **kwargs):
    #    if cls == NiraapadClient:
    #        raise TypeError("class NiraapadClient must be subclassed.")
    #    return object.__new__(cls, *args, **kwargs)

    @staticmethod
    def connect_to_middlebox(host, port, keysdir=None):
        if NiraapadClient.niraapad_client_helper != None:
            del NiraapadClient.niraapad_client_helper
        NiraapadClient.niraapad_client_helper = NiraapadClientHelper(host, port, keysdir)

    @staticmethod
    def static_method(backend_type, *args, **kwargs):
        method_name = utils.CALLER_METHOD_NAME()

        module_name = importlib.import_module(
            utils.BACKENDS.modules[backend_type])
        class_name = getattr(module_name, backend_type)

        if NiraapadClient.mo == utils.MO.DIRECT:
            return getattr(class_name, method_name)(*args, **kwargs)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            return NiraapadClient.niraapad_client_helper.static_method(
                backend_type, method_name, pickle.dumps(args),
                pickle.dumps(kwargs))

        resp = getattr(class_name, method_name)(*args, **kwargs)
        NiraapadClient.niraapad_client_helper.static_method_trace(
            backend_type, method_name, pickle.dumps(args),
            pickle.dumps(kwargs), pickle.dumps(resp))
        return resp

    def initialize(self, *args, **kwargs):
        # Since the __init__ function is invoked similar to static methods,
        # that is, it is invoked using the class name, this function is
        # analogous to the static_method function above, except that we do not
        # need a variable for the method name, which is known to be "__init__"
        # in this case.

        module_name = importlib.import_module(
            utils.BACKENDS.modules[self.backend_type])
        class_name = getattr(module_name, self.backend_type)

        if NiraapadClient.mo == utils.MO.DIRECT or \
           NiraapadClient.mo == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            self.backend_instance = class_name(*args, **kwargs)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            self.backend_instance_id = \
                NiraapadClient.niraapad_client_helper.initialize(
                    self.backend_type, pickle.dumps(args), pickle.dumps(kwargs))

        if NiraapadClient.mo == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            self.backend_instance_id = \
                NiraapadClient.niraapad_client_helper.initialize_trace(
                    self.backend_type, pickle.dumps(args), pickle.dumps(kwargs))

    def generic_method(self, *args, **kwargs):
        # For any generic class instance method, the logic is similar to that
        # of any generic static method, except that the method is invoked using
        # the class instance name and not directly using the class name.
        # Thus, the following set of statements is analogous to the function
        # definition of the static_methods function above, except that we deal
        # with specific class instances identified using their unique
        # identifiers ("backend_instance_id"), which were set during
        # initialization.

        method_name = utils.CALLER_METHOD_NAME()

        if NiraapadClient.mo == utils.MO.DIRECT:
            return getattr(self.backend_instance, method_name)(*args, **kwargs)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            return NiraapadClient.niraapad_client_helper.generic_method(
                self.backend_type, self.backend_instance_id, method_name,
                pickle.dumps(args), pickle.dumps(kwargs))

        resp = getattr(self.backend_instance, method_name)(*args, **kwargs)
        NiraapadClient.niraapad_client_helper.generic_method_trace(
            self.backend_type, self.backend_instance_id, method_name,
            pickle.dumps(args), pickle.dumps(kwargs), pickle.dumps(resp))
        
        return resp

    def generic_getter(self):
        # Getter functions are an extremely simplified version of GenericMethod
        # since they are interpreted not as functions but as variables, which
        # may be used in an expression; in this case, we simply return the
        # variable value.

        property_name = utils.CALLER_METHOD_NAME()

        if NiraapadClient.mo == utils.MO.DIRECT:
            return getattr(self.backend_instance, property_name)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            return NiraapadClient.niraapad_client_helper.generic_getter(
                self.backend_type, self.backend_instance_id, property_name)

        resp = getattr(self.backend_instance, property_name)
        NiraapadClient.niraapad_client_helper.generic_getter_trace(
            self.backend_type, self.backend_instance_id, property_name,
            pickle.dumps(resp))

        return resp
            
    def generic_setter(self, value):
        # Setter functions are the opposite of getter functions. They simply
        # assign the provided value to the specified property.

        property_name = utils.CALLER_METHOD_NAME()

        if NiraapadClient.mo == utils.MO.DIRECT:
            setattr(self.backend_instance, property_name, value)
            return 

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            NiraapadClient.niraapad_client_helper.generic_setter(
                self.backend_type, self.backend_instance_id, property_name,
                pickle.dumps(value))
            return

        setattr(self.backend_instance, property_name, value)
        NiraapadClient.niraapad_client_helper.generic_setter_trace(
            self.backend_type, self.backend_instance_id, property_name,
            pickle.dumps(value))

        return
