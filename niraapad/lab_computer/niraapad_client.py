import os
import grpc
import pickle

import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc
import niraapad.shared.utils as utils

file_path = os.path.dirname(os.path.abspath(__file__))
default_keysdir = file_path + "/../keys/"

class NiraapadClientHelper:
    """
    The NiraapadClientHelper class encapsulates a gRPC client, which forwards all
    calls from class Serial on Lab Computer to the middlebox, which in turn is
    connected to the modules via actual serial communication. Unlike class
    Serial, there is only one global instance of class NiraapadClientHelper.
    """

    def __init__(self, host, port, keysdir=None):

        self.keysdir = default_keysdir
        if keysdir != None: self.keysdir = keysdir
        server_crt_path = os.path.join(self.keysdir, "server.crt")

        print("NiraapadClientHelper::__init__", host, port)
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
        print("NiraapadClientHelper::initialize", backend_type)
        resp = self.stub.Initialize(niraapad_pb2.InitializeReq(
            backend_type=backend_type,
            backend_instance_id=self.backend_instance_count,
            args=args_pickled,
            kwargs=kwargs_pickled))
        print("NiraapadClientHelper::initialized", backend_type)
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
    #    if cls is NiraapadClient:
    #        raise TypeError("class NiraapadClient must be subclassed.")
    #    return object.__new__(cls, *args, **kwargs)

    @staticmethod
    def start_niraapad_client_helper(host, port, keysdir=None):
        if NiraapadClient.niraapad_client_helper != None:
            del NiraapadClient.niraapad_client_helper
        NiraapadClient.niraapad_client_helper = NiraapadClientHelper(host, port, keysdir)

    @staticmethod
    def static_method(func_arg_names, backend_type, *args, **kwargs):
        method_name = utils.CALLER_METHOD_NAME()

        if backend_type is utils.BACKEND_SERIAL:
            from ftdi_serial import Serial as DirectSerial
        elif backend_type is utils.BACKEND_UR3_ARM:
            from hein_robots.universal_robots.ur3 import UR3Arm as DirectUR3Arm
        else:
            assert(False)

        # For example, if the caller is Serial.list_devices(...),
        # then we want to find the list of arguments (in string form) that the
        # same function in the original class DirectSerial takes, which we can
        # compute using Python's getfullargspec method, i.e., using
        # "inspect.getfullargsepc(DirectSerial.list_devices).args".
        # We generate and evaluate this command automatically, as follows:
        # (see how the func_arg_names term is derived)

        # Next, if we want to invoke the respective method in the original
        # class, say DirectSerial.list_devices(...) locally itself,
        # without going through the RPC, as is the case for modes MO.DIRECT
        # and MO.DIRECT_PLUS_MIDDLEBOX, we generate and evaluate the method
        # call string "DirectSerial.list_devices(...)" automatically.
        method_call_string = utils.generate_method_call_string(
            backend_type, method_name, func_arg_names, args, kwargs)

        if NiraapadClient.mo == utils.MO.DIRECT:
            return eval(method_call_string)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            return NiraapadClient.niraapad_client_helper.static_method(
                backend_type, method_name, pickle.dumps(args),
                pickle.dumps(kwargs))

        resp = eval(method_call_string)
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

        if self.backend_type is utils.BACKEND_SERIAL:
            from ftdi_serial import Serial as DirectSerial
        elif self.backend_type is utils.BACKEND_UR3_ARM:
            from hein_robots.universal_robots.ur3 import UR3Arm as DirectUR3Arm
        else:
            assert(False)

        func_arg_names = self.get_func_arg_names("__init__")
        init_call_string = utils.generate_init_call_string(
            self.backend_type, func_arg_names, args, kwargs)

        if NiraapadClient.mo == utils.MO.DIRECT or \
           NiraapadClient.mo == utils.MO.DIRECT_PLUS_MIDDLEBOX:
            self.backend_instance = eval(init_call_string)

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

        func_arg_names = self.get_func_arg_names(method_name)
        method_call_string = utils.generate_method_call_string(
            "self.backend_instance", method_name, func_arg_names, args, kwargs)

        if NiraapadClient.mo == utils.MO.DIRECT:
            return eval(method_call_string)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            return NiraapadClient.niraapad_client_helper.generic_method(
                self.backend_type, self.backend_instance_id, method_name,
                pickle.dumps(args), pickle.dumps(kwargs))

        resp = eval(method_call_string)
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
        getter_call_string = utils.generate_getter_call_string(
            "self.backend_instance", property_name)

        if NiraapadClient.mo == utils.MO.DIRECT:
            return eval(getter_call_string)

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            return NiraapadClient.niraapad_client_helper.generic_getter(
                self.backend_type, self.backend_instance_id, property_name)

        resp = eval(getter_call_string)
        NiraapadClient.niraapad_client_helper.generic_getter_trace(
            self.backend_type, self.backend_instance_id, property_name,
            pickle.dumps(resp))

        return resp
            
    def generic_setter(self, value):
        # Setter functions are the opposite of getter functions. They simply
        # assign the provided value to the specified property.

        property_name = utils.CALLER_METHOD_NAME()
        setter_call_string = utils.generate_setter_call_string(
            "self.backend_instance", property_name)

        if NiraapadClient.mo == utils.MO.DIRECT:
            exec(setter_call_string)
            return 

        if NiraapadClient.mo == utils.MO.VIA_MIDDLEBOX:
            NiraapadClient.niraapad_client_helper.generic_setter(
                self.backend_type, self.backend_instance_id, property_name,
                pickle.dumps(value))
            return

        exec(setter_call_string)
        NiraapadClient.niraapad_client_helper.generic_setter_trace(
            self.backend_type, self.backend_instance_id, property_name,
            pickle.dumps(value))

        return
