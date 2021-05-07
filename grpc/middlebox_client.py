import grpc
import middlebox_pb2
import middlebox_pb2_grpc

DeviceWriteHandler = Callable[[int, 'Device'], None]

class SerialDeviceInfo:
    """
    The SerialDeviceInfo class is a basic data structure that contains information about connected serial devices
    """

    def __init__(self,
                 index: Optional[int]=None,
                 serial: Union[bytes, str]='',
                 port: Optional[str]=None,
                 description: Optional[Union[bytes, str]]=None,
                 **kwargs) -> None:
        """
        The SerialDeviceInfo class is a basic data structure that contains information about connected serial devices

        :param index: index number
        :param serial: device serial number, if available
        :param description: device description
        """
        self.index = index
        self.serial = serial.decode() if isinstance(serial, bytes) else serial
        self.port = port
        self.description = description.decode() if isinstance(description, bytes) else description

class MiddleboxClient:
    """
    The MiddleboxClient class encapsulates a gRPC client, which forwards all calls
    from class VirtualSerial to the middlebox, which in turn is connected to 
    the modules via actual serial communication. Unlike class VirtualSerial,
    there is only one instance of class MiddleboxClient.
    """

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = middlebox_pb2_grpc.MiddleboxStub(channel)
        self.num_devices = 0

    def list_devices(self) -> List[SerialDeviceInfo]:
        """
        Get a list of SerialDeviceInfo instanes with information about serial devices connected to the middlebox

        :return: list of SerialDeviceInfo instances
        """
        request = middlebox_pb2.ListDevicesRequest()
        response = self.stub.ListDevices(request)
        unpacked_response = []
        for device_info in response.devices_info:
            index = None if device_info.index == "" else int(device_info.index)
            serial = device_info.serial
            port = None if device_info.port == "" else device_info.port
            description = None if device_info.description == "" else device_info.description
            SerialDeviceInfo unpacked_device_info(index, serial, port, description)
            unpacked_response.append(unpacked_device_info)
            
        return unpacked_response

    def list_device_ports(self) -> List[str]:
        """
        Get a list of COM port strings for connected serial devices

        :return: List of COM port strings
        """
        request = middlebox_pb2.ListDevicePortsRequest()
        response = self.stub.ListDevicePorts(request)
        return response.ports

    def list_device_serials(self) -> List[str]:
        """
        Get a list of device serial numbers for connected FTDI devices

        :return: List of device serial number strings
        """
        request = middlebox_pb2.ListDeviceSerialsRequest()
        response = self.stub.ListDeviceSerials(request)
        return response.serial_numbers

    def initialize(self,
                   device: Optional[SerialDeviceType]=None,
                   device_serial: Optional[str]=None,
                   device_number: Optional[int]=None,
                   device_port: Optional[str]=None,
                   baudrate: int=115200,
                   parity: int=PARITY_NONE,
                   stop_bits: int=STOP_BITS_1,
                   data_bits: int=DATA_BITS_8,
                   read_timeout: NumberType=5,
                   write_timeout: NumberType=5,
                   connect_timeout: Optional[NumberType]=30,
                   connect_retry: bool=True,
                   connect_settle_time: NumberType=3,
                   connect: bool=True):
        self.num_devices += 1
        
        if device is None: device = ""
        device_type_format = middlebox_pb2.SerialDeviceType.Format.STRING
        if type(device) is int:
            device_type_format = middlebox_pb2.SerialDeviceType.Format.INT
            device = str(device)

        request = middlebox_pb2.InitializeRequest(
            self.num_devices,
            middlebox_pb2.SerialDeviceType(device_type_format, device),
            (device_serial if device_serial != None else ""),
            (str(device_number) if device_number != None else ""),
            (device_port if device_port != None else ""),
            baudrate,
            parity,
            stop_bits,
            data_bits,
            float(read_timeout),
            float(writ_timeout),
            float(connect_timeout),
            connect_retry,
            connect_settle_time,
            connect)
        response = self.stub.Initialize(request)

        return self.num_devices
    
    def connect(self, device_id):
        request = middlebox_pb2.ConnectRequest(device_id)
        response = self.stub.Connect(request)

    def disconnect(self, device_id):
        request = middlebox_pb2.DisconnectRequest(device_id)
        response = self.stub.Disconnect(request)

    def set_parameters(self, device_id, baudrate, parity, stop_bits, data_bits):
        baudrate = str(baudrate) if baudrate != None else ""
        parity = str(parity) if parity != None else ""
        stop_bits = str(stop_bits) if stop_bits != None else ""
        data_bits = str(data_bits) if data_bits != None else ""
        request = middlebox_pb2.SetParametersRequest(device_id, baudrate,
                                                     parity, stop_bits,
                                                     data_bits)
        response = self.stub.SetParameters(request)

    def update_timeouts(self, device_id):
        request = middlebox_pb2.UpdateTimeoutsRequest(device_id)
        response = self.stub.UpdateTimeouts(request)

    def info(self, device_id):
        request = middlebox_pb2.InfoRequest(device_id)
        response = self.stub.Info(request)
        return response.device_info

    def serial_number(self, device_id):
        request = middlebox_pb2.SerialNumberRequest(device_id)
        response = self.stub.SerialNumber(request)
        if response.device_serial == "": return None
        else return response.device_serial

    def read(self, device_id, num_bytes, timeout):
        num_bytes = str(num_bytes) if num_bytes =! None else ""
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.ReadRequest(device_id, num_bytes, timeout)
        response = self.stub.Read(request)
        return response.data

    def read_line(self, device_id, line_ending, timeout):
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.ReadLineRequest(device_id, line_ending, timeout)
        response = self.stub.ReadLine(request)
        return response.data

    def write(self, device_id, data, timeout):
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.WriteRequest(device_id, data, timeout)
        response = self.stub.Write(request)
        return response.num_bytes

    def request(self, device_id, data, timeout, line_ending):
        timeout = str(timeout) if timeout != None else ""
        request = middlebox_pb2.RequestRequest(device_id, data, timeout, line_ending)
        response = self.stub.Request(request)
        return response.data
