import os
import grpc
import pickle

import niraapad.protos.n9_pb2 as n9_pb2
import niraapad.protos.n9_pb2_grpc as n9_pb2_grpc

from niraapad.shared.ftdi_serial import SerialDeviceInfo
from niraapad.shared.utils import *

file_path = os.path.dirname(os.path.abspath(__file__))
default_keys_path = file_path + "/../keys/"

class N9Client:
    """
    The N9Client class encapsulates a gRPC client, which forwards all
    calls from class Serial on Lab Computer to the middlebox, which in turn is
    connected to the modules via actual serial communication. Unlike class
    Serial, there is only one global instance of class N9Client.
    """

    def __init__(self, host, port, keys_path=None):

        self.keys_path = default_keys_path
        if keys_path != None: self.keys_path = keys_path

        with open(keys_path + 'server.crt', 'rb') as f:
            trusted_certs = f.read()
        client_credentials = grpc.ssl_channel_credentials(
            root_certificates=trusted_certs)
        channel = grpc.secure_channel(host + ':' + port, client_credentials)
        self.stub = n9_pb2_grpc.N9Stub(channel)

        self.num_devices = 0

    def static_method(self, method_name, args_pickled, kwargs_pickled):
        try:
            resp = self.stub.StaticMethod(
                n9_pb2.StaticMethodReq(
                    method_name=method_name,
                    args=args_pickled,
                    kwargs=kwargs_pickled))
            return pickle.loads(resp.resp)
        except Exception as e:
            print("Exception:", e)
            assert(False)

    def static_method_trace(self, method_name, args_pickled, kwargs_pickled,
                      resp_pickled):
        self.stub.StaticMethodTrace(
            n9_pb2.StaticMethodTraceMsg(
                req=n9_pb2.StaticMethodReq(
                    method_name=method_name,
                    args=args_pickled,
                    kwargs=kwargs_pickled),
                resp=n9_pb2.StaticMethodResp(
                    resp=resp_pickled)))

    def initialize(self, args_pickled, kwargs_pickled):
        self.num_devices += 1
        self.stub.Initialize(
            n9_pb2.InitializeReq(
                device_id=self.num_devices,
                args=args_pickled,
                kwargs=kwargs_pickled))
        return self.num_devices

    def initialize_trace(self, args_pickled, kwargs_pickled):
        self.num_devices += 1
        self.stub.InitializeTrace(
            n9_pb2.InitializeTraceMsg(
                req=n9_pb2.InitializeReq(
                    device_id=self.num_devices,
                    args=args_pickled,
                    kwargs=kwargs_pickled),
                resp=n9_pb2.InitializeResp()))
        return self.num_devices

    def device_specific_method(self, device_id, method_name, args_pickled,
                               kwargs_pickled):
        resp = self.stub.DeviceSpecificMethod(
            n9_pb2.DeviceSpecificMethodReq(
                device_id=device_id,
                method_name=method_name,
                args=args_pickled,
                kwargs=kwargs_pickled))
        return pickle.loads(resp.resp)

    def device_specific_method_trace(self, device_id, method_name, args_pickled,
                                     kwargs_pickled, resp_pickled):
        self.stub.DeviceSpecificMethodTrace(
            n9_pb2.DeviceSpecificMethodTraceMsg(
                req=n9_pb2.DeviceSpecificMethodReq(
                    device_id=device_id,
                    method_name=method_name,
                    args=args_pickled,
                    kwargs=kwargs_pickled),
                resp=n9_pb2.DeviceSpecificMethodResp(
                    resp=resp_pickled)))

    def device_specific_getter(self, device_id, property_name):
        resp = self.stub.DeviceSpecificGetter(
            n9_pb2.DeviceSpecificGetterReq(
                device_id=device_id,
                property_name=property_name))
        return pickle.loads(resp.resp)

    def device_specific_getter_trace(self, device_id, property_name,
                                     resp_pickled):
        self.stub.DeviceSpecificGetterTrace(
            n9_pb2.DeviceSpecificGetterTraceMsg(
                req=n9_pb2.DeviceSpecificGetterReq(
                    device_id=device_id,
                    property_name=property_name),
                resp=n9_pb2.DeviceSpecificGetterResp(
                    resp=resp_pickled)))

    def device_specific_setter(self, device_id, property_name, value_pickled):
        self.stub.DeviceSpecificSetter(
            n9_pb2.DeviceSpecificSetterReq(
                device_id=device_id,
                property_name=property_name,
                value=value_pickled))

    def device_specific_setter_trace(self, device_id, property_name,
                                     value_pickled):
        self.stub.DeviceSpecificSetterTrace(
            n9_pb2.DeviceSpecificSetterTraceMsg(
                req=n9_pb2.DeviceSpecificSetterReq(
                    device_id=device_id,
                    property_name=property_name,
                    value=value_pickled),
                resp=n9_pb2.DeviceSpecificSetterResp()))
