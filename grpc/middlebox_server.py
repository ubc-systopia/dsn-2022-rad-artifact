mport grpc
import middlebox_pb2
import middlebox_pb2_grpc
import serial

DeviceWriteHandler = Callable[[int, 'Device'], None]

class MiddleboxServicer(middlebox_pb2_grpc.MiddleboxServicer):
    """Provides methods that implement functionality of middlebox server."""

    def __init__(self):
        self.serial_objs = {}

    def ListDevices(self, request, context):
        devices_info = Serial.list_devices()
        devices_info_msg = []
        for device_info in devices_info:
            index = "" if device_info.index == None else device_info.index
            port = "" if device_info.port == None else device_info.port
            serial = device_info.serial
            description = "" if device_info.description == None else device_info.description
            devices_info_msg.append(middlebox_pb2.SerialDeviceInfo(index, serial, port, description))
        response = middlebox_pb2.ListDevicesResponse(devices_info_msg)
        return response

    def ListDevicePorts(self, request, context):
        device_ports = Serial.list_device_ports()
        response = middlebox_pb2.ListDevicePortsResponse(device_ports)
        return response

    def ListDeviceSerials(self, request, context):
        # TODO Fix parameter mismatch
        # Serial.list_device_serials expects an argument call "cls"
        # But we didn't provide any through gRPC!

        # Sending an empty response for now...
        response = middlebox_pb2.ListDeviceSerials(d)
        return response

    def Initialize(self, request, context):
        device_type = request.device_type.device_type
        if device_type == "": device_type = None
        elif request.device_type.format == request.device_type.Format.INT:
            device_type = int(device_type)

        device_serial = request.device_serial if request.device_serial != "" else None
        device_number = int(request.device_number) if request.device_number != "" else None
        device_port = request.device_port if request.device_port != "" else None

        self.serial_objs[request.device_id] = Serial(device_type,
                                              device_serial,
                                              device_number,
                                              device_port,
                                              request.baudrate,
                                              request.parity,
                                              request.stop_bits,
                                              request.data_bits,
                                              request.read_timeput,
                                              request.write_timeout,
                                              request.connect_timeout,
                                              request.connect_retry,
                                              request.connect_settle_time,
                                              request.connect)

        response = middlebox_pb2.InitializeResponse()
        return response

    def Connect(self, request, context):
        self.serial_objs[request.device_id].connect()
        response = middlebox_pb2.ConnectResponse()
        return response

    def Disconnect(self, request, context):
        self.serial_objs[request.device_id].disconnect()
        response = middlebox_pb2.DisconnectResponse()
        return response

    def SetParameters(self, request, context):
        baudrate = request.baudrate if request.baudrate != "" else None
        parity = request.parity if request.parity != "" else None
        stop_bits = request.stop_bits if request.stop_bits != "" else None
        data_bits = request.data_bits if request.data_bits != "" else None
        self.serial_objs[request.device_id].set_parameters(baudrate, parity, stop_bits, data_bits)
        response = middlebox_pb2.SetParametersResponse()
        return response

    def UpdateTimeouts(self, request, context):
        self.serial_objs[request.device_id].update_timeouts()
        response = middlebox_pb2.UpdateTimeoutsResponse()
        return response

    def Info(self, request, context):
        device_info = self.serial_objs[request.device_id].info()
        if device_info.index == None: device_info.index = ""
        if device_info.port == None: device_info.port = ""
        if device_info.description == None: device_info.description = ""
        device_info_msg = middlebox_pb2.SerialDeviceInfo(str(device_info.index),
                                                         device_info.serial,
                                                         device_info.port,
                                                         device_info.description)
        response = middlebox_pb2.InfoResponse(device_info_msg)
        return response

    def SerialNumber(self, request, context):
        device_serial = self.serial_objs[request.device_id].serial_number()
        if device_serial == None: serial_number = ""
        response = middlebox_pb2.SerialNumberResponse(device_serial)
        return response

    def Read(self, request, context):
        num_bytes = None if request.num_bytes == "" else int(request.num_bytes)
        timeout = None if request.timeout == "" else float(request.timeout)
        data = self.serial_objs[request.device_id].read(num_bytes, timeout)
        response = middlebox_pb2.Read(data)
        return response

    def ReadLine(self, request, context):
        timeout = None if request.timeout == "" else float(request.timeout)
        data = self.serial_objs[request.device_id].read_line(request.line_ending, timeout)
        response = middlebox_pb2.ReadLine(data)
        return response

    def Write(self, request, context):
        timeout = None if request.timeout == "" else float(request.timeout)
        num_bytes = self.serial_objs[request.device_id].write(request.data, timeout)
        response = middlebox_pb2.Write(num_bytes)
        return response

    def Request(self, request, context):
        timeout = None if request.timeout == "" else float(request.timeout)
        data = self.serial_objs[request.device_id].request(request.data, timeout, request.line_ending)
        response = middlebox+pb2.Request(data)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    middlebox_pb2_grpc.add_MiddleboxServicer_to_server(MiddleboxServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == ' __main__':
    serve()
