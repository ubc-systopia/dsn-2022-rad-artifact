import os
# add current directory to path so we can load ftd2xx DLL files
os.environ['PATH'] = os.environ['PATH'] + ';' + os.path.dirname(__file__)
import time
from typing import Any, Union, List, Optional, Callable
from ctypes import c_void_p
import serial as pyserial
from serial.tools.list_ports import comports
from serial.rs485 import RS485Settings
import atexit

try:
    from ftd2xx import FTD2XX
    import ftd2xx
    FTD2XX_AVAILABLE = True
except ImportError:
    ftd2xx = {}
    FTD2XX_AVAILABLE = False
    FTD2XX = Any

SerialDeviceType = Union[str, int, 'Device']
NumberType = Union[float, int]
DeviceWriteHandler = Callable[[int, 'Device'], None]


class SerialException(Exception):
    """ Base exception for Serial errors """
    pass


class SerialInvalidDeviceException(SerialException):
    """ Invalid Serial device error """
    pass


class SerialDeviceOpenException(SerialException):
    """ Error opening device """
    pass


class SerialTimeoutException(SerialException):
    """ Serial timeout error """
    pass


class SerialReadTimeoutException(SerialTimeoutException):
    """ Serial read timeout error """
    pass


class SerialWriteTimeoutException(SerialTimeoutException):
    """ Serial write timeout error """
    pass


class SerialDeviceNotImplementedException(SerialException):
    """ Serial device not implemented error """
    pass


class SerialFtd2xxNotAvailableException(SerialException):
    pass


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


class Device:
    """
    The Device class is a base class used to communicate with different serial devices. Different Device subclasses
    are used for different device types, including FTDI devices and basic PySerial devices.
    """
    def __init__(self):
        self.write_handlers: List[DeviceWriteHandler] = []
        self.read_timeout = 1.0
        self.write_timeout = 1.0

    def add_write_handler(self, handler: DeviceWriteHandler):
        self.write_handlers.append(handler)

    def close(self):
        pass

    def clear(self):
        pass

    def purge(self):
        self.clear()

    def reset(self):
        self.clear()

    def set_baud_rate(self, baudrate: int):
        pass

    def set_parameters(self, data_bits: int, stop_bits: int, parity_bits: int):
        pass

    def set_timeouts(self, read_timeout: float, write_timeout: float):
        self.read_timeout = read_timeout / 1000
        self.write_timeout = write_timeout / 1000

    def get_input_size(self) -> int:
        return 0

    def get_output_size(self) -> int:
        return 0

    def write(self, data: bytes):
        for handler in self.write_handlers:
            handler(data, self)

    def read(self, num_bytes: int, raw: bool=True) -> bytes:
        return bytes()

    def read_all(self) -> bytes:
        return self.read(self.get_input_size())

    def enable_write_log(self, enable: bool=True):
        self.write_log_enable = enable

    def get_write_log(self):
        return self.write_log

    def clear_write_log(self):
        self.write_log = bytes()

    def set_bit_mode(self, mask: int, enable: bool):
        raise SerialDeviceNotImplementedException(f'set_bit_mode not available on {self.__class__.__name__} devices')


class MockDevice(Device):
    def __init__(self, input_buffer: Optional[bytes]=None):
        Device.__init__(self)
        self.input_buffer = b'' if input_buffer is None else input_buffer
        self.output_buffer = b''

    def close(self):
        self.clear()

    def clear(self):
        self.input_buffer = b''
        self.output_buffer = b''

    def get_input_size(self):
        return len(self.input_buffer)

    def write(self, data: bytes):
        self.output_buffer += data

    def read(self, num_bytes: int, raw: bool=True):
        data = self.input_buffer[:num_bytes]
        self.input_buffer = self.input_buffer[num_bytes:]

        return data


class FtdiDevice(Device):
    def __init__(self, device_serial: Optional[str]=None, device_number: Optional[int] = None):
        Device.__init__(self)

        if not FTD2XX_AVAILABLE:
            raise SerialFtd2xxNotAvailableException(f'FTD2XX package not installed')

        try:
            if device_serial is not None:
                self.ftdi = ftd2xx.openEx(device_serial.encode())
            elif device_number is not None:
                self.ftdi = ftd2xx.open(int(device_number))
            else:
                self.ftdi = ftd2xx.open()
        except ftd2xx.DeviceError:
            raise SerialDeviceOpenException(f'Error opening FTDI serial device')

    def close(self):
        try:
            self.ftdi.close()
        except ftd2xx.DeviceError:
            pass

    def clear(self):
        self.ftdi.purge()

    def reset(self):
        self.ftdi.resetDevice()
        self.ftdi.resetPort()

    def set_baud_rate(self, baudrate: int):
        self.ftdi.setBaudRate(baudrate)

    def set_timeouts(self, read_timeout: float, write_timeout: float):
        self.ftdi.setTimeouts(read_timeout, write_timeout)

    def set_parameters(self, data_bits: int, stop_bits: int, parity_bits: int):
        self.ftdi.setDataCharacteristics(data_bits, stop_bits, parity_bits)

    def get_input_size(self) -> int:
        return self.ftdi.getStatus()[0]

    def get_output_size(self) -> int:
        return self.ftdi.getStatus()[1]

    def write(self, data: bytes):
        super().write(data)
        self.ftdi.write(data)

    def read(self, num_bytes: int, raw: bool = True) -> bytes:
        return self.ftdi.read(num_bytes, raw)

    def set_bit_mode(self, mask: int, enable: bool):
        self.ftdi.setBitMode(mask, enable)


class PySerialDevice(Device):
    PARITIES = {
        0: pyserial.PARITY_NONE,
        1: pyserial.PARITY_ODD,
        2: pyserial.PARITY_EVEN
    }

    STOP_BITS = {
        0: pyserial.STOPBITS_ONE,
        2: pyserial.STOPBITS_TWO
    }

    def __init__(self, device_port: str):
        Device.__init__(self)
        self.serial = pyserial.Serial(device_port)
        try:
            self.serial.rs485_mode = RS485Settings()
        except ValueError:
            # setting RS485 mode fails on the Raspberry Pi
            self.serial.rs485_mode = None

    def close(self):
        self.serial.close()

    def clear(self):
        self.serial.flush()

    def reset(self):
        pass

    def set_baud_rate(self, baudrate: int):
        self.serial.baudrate = baudrate

    def set_timeouts(self, read_timeout: float, write_timeout: float):
        self.serial.timeout = read_timeout / 1000
        self.serial.write_timeout = write_timeout / 1000

    def set_parameters(self, data_bits: int, stop_bits: int, parity_bits: int):
        self.serial.bytesize = data_bits
        self.serial.stopbits = self.STOP_BITS[stop_bits]
        self.serial.parity = self.PARITIES[parity_bits]

    def get_input_size(self) -> int:
        return self.serial.in_waiting

    def get_output_size(self) -> int:
        return self.serial.out_waiting

    def write(self, data: bytes):
        super().write(data)
        self.serial.write(data)

    def read(self, num_bytes: int, raw: bool = True) -> bytes:
        return self.serial.read(num_bytes)


class DirectSerial:
    """
    The Serial class can be used to create a connection to a serial device
    """
    # FT_STATUS
    FT_OK = 0

    # FT_Purge
    FT_PURGE_RX = 1
    FT_PURGE_TX = 2

    PARITY_NONE = 0
    PARITY_ODD = 1
    PARITY_EVEN = 2

    STOP_BITS_1 = 0
    STOP_BITS_2 = 2

    DATA_BITS_7 = 7
    DATA_BITS_8 = 8

    @staticmethod
    def list_devices() -> List[SerialDeviceInfo]:
        """
        Get a list of SerialDeviceInfo instanes with information about serial devices connected to the computer

        :return: list of SerialDeviceInfo instances
        """

        if FTD2XX_AVAILABLE:
            devices = ftd2xx.listDevices()

            if devices is None:
                return []

            num_devices = len(devices)
            return [SerialDeviceInfo(**ftd2xx.getDeviceInfoDetail(i)) for i in range(0, num_devices)]
        else:
            return [SerialDeviceInfo(port=p.device, description=p.description) for p in comports()]

    @staticmethod
    def list_device_ports() -> List[str]:
        """
        Get a list of COM port strings for connected serial devices

        :return: List of COM port strings
        """
        return [info.device for info in comports()]

    @classmethod
    def list_device_serials(cls) -> List[str]:
        """
        Get a list of device serial numbers for connected FTDI devices

        :return: List of device serial number strings
        """
        return [device.serial for device in cls.list_devices() if device.serial]

    def __init__(self,
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
                 connect: bool=True) -> None:
        """
        :param device: [Optional] Device instance to use for communication
        :param device_serial: [Optional] FTDI Device serial number to use when creating a connection
        :param device_number: [Optional] The index number of the FTDI device to connect to, ``device_serial`` should be used when possible
        :param device_port: [Optional] COM port string of the device. If given, PySerial will be used for communication
        :param baudrate: [Optional] baudrate to use for serial connection, defaults to 115200
        :param parity: [Optional] serial connection parity, one of ``Serial.PARITY_NONE``, ``Serial.PARITY_EVEN``, ``Serial.PARITY_ODD``; defaults to ``Serial.PARITY_NONE``
        :param stop_bits: [Optional] number of stop bits for serial connection, one of ``Serial.STOP_BITS_1``, or ``Serial.STOP_BITS_2``; defualts to ``Serial.STOP_BITS_1``
        :param data_bits: [Optional] number of data bits for serial connection, one of ``Serial.DATA_BITS_7`` or ``Serial.DATA_BITS_8``; defaults to ``Serial.DATA_BITS_8``
        :param read_timeout: [Optional] number of seconds to wait for data when reading from serial connection, defaults to 5s
        :param write_timeout: [Optional] number of seconds to wait for confirmation after writing data, defaults to 5s
        :param connect_timeout: [Optional] amount of time to wait for a serial connection to be made, defaults to 30s
        :param connect_retry: [Optional] keep retrying connection until successful if True, defaults to True
        :param connect_settle_time: [Optional] amount of time to wait after connection before setup, defaults to 3
        :param connect: [Optional] automatically connect to the device when created if True, defaults to True
        """
        self.device = device
        self.device_serial = device_serial
        self.device_number = device_number
        self.device_port = device_port

        # check to see if we were passed something other then a Device as the first parameter
        if self.device is not None and not isinstance(self.device, Device):
            if isinstance(self.device, int) or isinstance(self.device, float):
                self.device_serial = self.device
            elif isinstance(self.device, str):
                # if the "device" string starts with 'COM' or a '/' assume it is a pyserial device
                if self.device.lower().startswith(('com', '/')):
                    self.device_port = self.device
                else:
                    self.device_serial = self.device
            elif isinstance(self.device, pyserial.Serial):
                self.device = PySerialDevice(self.device)
            elif isinstance(self.device, Serial):
                self.device = self.device.device
            else:
                raise SerialInvalidDeviceException(f'Invalid serial device: {self.device}')

            self.device = None

        self.baudrate = baudrate
        self.data_bits = data_bits
        self.parity = parity
        self.stop_bits = stop_bits
        self.read_timeout_value = read_timeout
        self.write_timeout_value = write_timeout
        self.connect_timeout = connect_timeout
        self.connect_retry = connect_retry
        self.connect_settle_time = connect_settle_time
        self.input_buffer = b''
        self.output_buffer = b''
        self.connected = False

        if connect:
            self.connect()

        atexit.register(self.disconnect)

    def open_device(self):
        if self.device is not None:
            return
        elif self.device_port is not None:
            self.device = PySerialDevice(self.device_port)
        else:
            self.device = FtdiDevice(self.device_serial, self.device_number)

    def connect(self):
        """
        Connect to the serial device if a connection hasn't been made (this is not needed in most cases)
        """
        if self.connected:
            return

        first = True
        start_time = time.time()
        while first or (self.connect_retry and self.device is None):
            try:
                self.open_device()
                # if we weren't able to connect right way, we'll have to wait for the device to settle
                if not first:
                    # wait for the device to settle down
                    time.sleep(self.connect_settle_time)
                    # purge the read buffer to get rid of any bad data accumulated during connection
                    self.device.clear()
                    self.init_device()
            except SerialDeviceOpenException:
                time.sleep(0.5)

            connect_time = time.time() - start_time

            if self.device is None and connect_time >= self.connect_timeout:
                raise SerialTimeoutException('Timeout while connecting to device')

            first = False

        #time.sleep(0.5)
        self.init_device()
        self.connected = True

    def disconnect(self):
        """
        Disconnect the serial device
        """
        if not self.connected:
            return

        self.device.close()
        self.connected = False

    def init_device(self):
        self.device.reset()
        self.device.set_baud_rate(self.baudrate)
        self.device.set_parameters(self.data_bits, self.stop_bits, self.parity)
        self.update_timeouts()

    def set_parameters(self, baudrate: Optional[int]=None, parity: Optional[int]=None, stop_bits: Optional[int]=None, data_bits: Optional[int]=None):
        """
        Change the serial connection parameters for the serial device
        """
        self.baudrate = baudrate if baudrate is not None else self.baudrate
        self.parity = parity if parity is not None else self.parity
        self.stop_bits = stop_bits if stop_bits is not None else self.stop_bits
        self.data_bits = data_bits if data_bits is not None else self.data_bits
        self.init_device()

    def update_timeouts(self):
        self.device.set_timeouts(int(self.read_timeout_value * 1000), int(self.write_timeout_value * 1000))

    @property
    def info(self) -> SerialDeviceInfo:
        """
        Get info about the connected serial device

        :return: SerialDeviceInfo instance
        """
        if self.device is None or not self.connected:
            raise SerialException('Cannot get device info, device is not connected')

        if isinstance(self.device, FtdiDevice):
            return SerialDeviceInfo(**self.device.ftdi.getDeviceInfo())

        return SerialDeviceInfo()

    @property
    def serial_number(self)-> str:
        """
        Get the serial number for the conneted device, if available

        :return: serial number string
        """
        if self.device is None or not self.connected:
            raise SerialException('Cannot get device serial, device is not connected')

        return self.info.serial

    @property
    def in_waiting(self) -> int:
        """
        Get the number of bytes waiting in the input buffer

        :return: number of bytes in the input buffer
        """
        if self.device is None or not self.connected:
            return 0

        return self.device.get_input_size() + len(self.input_buffer)

    @property
    def out_waiting(self) -> int:
        """
        Get the number of bytes waiting in the output buffer

        :return: number of bytes in the output buffer
        """
        if self.device is None or not self.connected:
            return 0

        return self.device.get_output_size()

    @property
    def read_timeout(self):
        """
        Get or set the read timeout
        """
        return self.read_timeout_value

    @read_timeout.setter
    def read_timeout(self, value):
        self.read_timeout_value = value
        self.update_timeouts()

    @property
    def write_timeout(self):
        """
        Get or set the write timeout
        """
        return self.write_timeout_value

    @write_timeout.setter
    def write_timeout(self, value):
        self.write_timeout_value = value
        self.update_timeouts()

    def read(self, num_bytes: int=None, timeout: Optional[NumberType]=None) -> bytes:
        """
        Read bytes from the serial device

        :param num_bytes: [Optional] number of bytes to read, defaults to reading the entire input buffer if not given (will wait for at least 1 byte if buffer empty)
        :param timeout: [Optional] read timeout to use while reading, will be reset to default afterwards

        :return: data bytes
        """
        if self.device is None or not self.connected:
            raise SerialException('Cannot read, device is not connected')

        if num_bytes is None:
            num_bytes = self.in_waiting

        if num_bytes == 0:
            return b''

        if num_bytes > len(self.input_buffer):
            if timeout is not None:
                old_timeout = self.read_timeout
                self.read_timeout = timeout

            serial_data = self.device.read(num_bytes - len(self.input_buffer))

            if timeout is not None:
                self.read_timeout = old_timeout

            if serial_data == b'' and num_bytes != len(self.input_buffer):
                raise SerialReadTimeoutException('Read timeout')

            data = self.input_buffer + serial_data
            self.input_buffer = b''
        else:
            data = self.input_buffer[:num_bytes]
            self.input_buffer = self.input_buffer[num_bytes:]

        return data

    def read_line(self, line_ending: bytes=b'\r', timeout: Optional[NumberType]=None) -> bytes:
        """
        Read a "line" of data from the serial device until the given line ending is found

        :param line_ending: the line ending byte(s) to look for, defaults to ``b'\\r'``
        :param timeout: the timeout to use while reading data, will be reset to default afterwards
        :return: bytes of data
        """
        if self.device is None or not self.connected:
            raise SerialException('Cannot read, device is not connected')

        line = b''
        ending_length = len(line_ending)
        while True:
            num_bytes = self.in_waiting
            # always read at least len(line_ending) bytes
            bytes_to_read = num_bytes if num_bytes != 0 else 1
            data = self.read(bytes_to_read, timeout=timeout)
            line += data
            try:
                ending_index = line.index(line_ending)
                [line_data, remaining] = [line[:ending_index], line[ending_index + ending_length:]]
                self.input_buffer += remaining
                return line_data
            except ValueError:
                pass

    def write(self, data: Union[bytes, str], timeout: Optional[NumberType]=None) -> int:
        """
        Write the given data to the serial device

        :param data: a string or bytes of data to write
        :param timeout: [Optional] timeout to use when writing data, will be reset to default

        :return: number of bytes written
        """
        if self.device is None or not self.connected:
            raise SerialException('Cannot write, device is not connected')

        if isinstance(data, str):
            data = data.encode()

        if timeout is not None:
            old_timeout = self.write_timeout
            self.write_timeout = timeout

        num_bytes = self.device.write(data)

        if timeout is not None:
            self.write_timeout = old_timeout

        return num_bytes

    def request(self, data: bytes, timeout: Optional[NumberType]=None, line_ending: bytes=b'\r'):
        """
        Perform a "request", which writes the given data and then reads the "response" from the serial device until the
        given line ending is found

        :param data: request data to write
        :param timeout: [Optional] read timeout to use when reading response
        :param line_ending: [Optional] line ending byte(s) to look for in response, defaults to ``b'\\r'``
        :return: bytes of response data
        """
        self.write(data, timeout=timeout)
        return self.read_line(timeout=timeout, line_ending=line_ending)

    def flush(self):
        """
        Flush data from the input and output buffers
        """
        self.device.purge()

    def reset_input_buffer(self):
        """
        Flush / reset data in the input buffer
        """
        self.device.purge(self.FT_PURGE_RX)

    def reset_output_buffer(self):
        """
        Flush / reset data in the output buffer
        """
        self.device.purge(self.FT_PURGE_TX)

    def set_bit_mode(self, mask: int, enable: bool):
        """
        Enable or disable bit-bang mode on FTDI devices
        :param mask: bit mask for I/O direction (1 is output)
        :param enable: enables bit-bang mode if True, disables if False
        :return:
        """
        self.device.set_bit_mode(mask, enable)


################################################################################
################################################################################
########################## MODIFIED CODE STARTS HERE ###########################
################################################################################
################################################################################

from enum import Enum
from niraapad.lab_computer.middlebox_client import MiddleboxClient
from niraapad.shared.utils import MO

import inspect

# We define three different mode of operation (MOs)..
#
# Mode 1, DIRECT_SERIAL: This is the coventional mode, where requests are
# sent directly to the C9 and to other robot modules via serial communication
# (nothing really changes in this case).
#
# Mode 2, DIRECT_MIDDLEBOX: This is the mode that we eventually want, where
# requests are sent directly to the Middlebox over Ethernet, which in turn
# forwards them to the C9 and to other robot modules via serial communication
# (note that in this case, all modules are physically connected to the Middlebox
# and not to the Lab Computer).
#
# MOde 3, DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING: This is a temporary mode,
# where are sent directly to the C9 and to other robot modules via serial
# communication and the response is also fetched likewise, but at the same time
# all the requests and all the responses are also forwarded to the Middlebox
# for tracing purposes. This design also demonstrates that the version of
# "class Serial", which we define below, works seamlessely with the rest of the
# experiment scripts from Hein Lab and NOrth Robotics.

class Serial:
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Serial", which is renamed to "class DirectSerial" (see above). In addition,
    the class maintains three operation modes as summarized above along in
    "class MO". In order to do so, this class simply forwards
    each function call to the respective function call in the respective
    DirectSerial class object (class objects are not involved in the case of
    static functions), or to the respective function call in the global object
    of type "class MiddleboxClient" (which in turn invokes an RPC to the
    middlebox), or both.
    """
    mo = MO.DIRECT_SERIAL
    middlebox_client = MiddleboxClient(mo)

    #@staticmethod
    #def invoke_static_method(func_name, *args, **kwargs):
    #    if mo == MO.DIRECT_SERIAL:
    #        return getattr(DirectSerial, func_name)(args, kwargs)

    #    if mo == MO.DIRECT_MIDDLEBOX:
    #        return getattr(Serial.middlebox_client, func_name)(None, args, kwargs)

    #    assert mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING
    #    response = getattr(DirectSerial, func_name)(args, kwargs)
    #    try:
    #        getattr(Serial.middlebox_client, func_name)(response, args, kwargs)
    #    except:
    #        return response

    #def invoke_init_method(self, *args, **kwargs):
    #    if mo == MO.DIRECT_SERIAL:
    #        self.device_serial = getattr(DirectSerial, func_name)(args, kwargs)
    #        return

    #    if mo == MO.DIRECT_MIDDLEBOX:
    #        self.id = getattr(Serial.middlebox_client, "initialize")(
    #            None, args, kwargs)
    #        return

    #    assert mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING
    #    self.device_serial = getattr(DirectSerial, func_name)(args, kwargs)
    #    try:
    #        self.id = getattr(Serial.middlebox_client, "initialize")(
    #            response, args, kwargs)
    #    except:
    #        return

    #def invoke_method(self, func_name, *args, **kwargs):
    #    if mo == MO.DIRECT_SERIAL:
    #        return getattr(self.direct_serial, func_name)(args, kwargs)

    #    if mo == MO.DIRECT_MIDDLEBOX:
    #        return getattr(Serial.middlebox_client, func_name)(
    #            None, self.id, args, kwargs)

    #    assert mo == MO.DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING
    #    response = getattr(self.direct_serial, func_name)(args, kwargs)
    #    try:
    #        getattr(Serial.middlebox_client, func_name)(
    #            response, self.id, args, kwargs)
    #    except:
    #        return response

    @staticmethod
    def list_devices():

        if mo == MO.DIRECT_SERIAL:
            return DirectSerial.list_devices()

        if mo == MO.DIRECT_MIDDLEBOX:
            return Serial.middlebox_client.list_devices()

        response = DirectSerial.list_devices()
        try: Serial.middlebox_client.list_devices_trace(response)
        except: return response

    @staticmethod
    def list_device_ports():

        if mo == MO.DIRECT_SERIAL:
            return DirectSerial.list_device_ports()
        if mo == MO.DIRECT_MIDDLEBOX:
            return Serial.middlebox_client.list_device_ports()

        response = DirectSerial.list_device_ports()
        try: Serial.middlebox_client.list_device_ports(response)
        except: return response

    @classmethod
    def list_device_serials(cls):

        if mo == MO.DIRECT_SERIAL:
            return DirectSerial.list_device_serials()

        if mo == MO.DIRECT_MIDDLEBOX:
            return Serial.middlebox_client.list_device_serials()

        response = DirectSerial.list_device_serials()
        try: Serial.middlebox_client.list_device_serials(response)
        except: return response

    def __init__(self, 
                 device: Optional[SerialDeviceType]=None,
                 device_serial: Optional[str]=None,
                 device_number: Optional[int]=None,
                 device_port: Optional[str]=None,
                 baudrate: int=115200,
                 parity: int=DirectSerial.PARITY_NONE,
                 stop_bits: int=DirectSerial.STOP_BITS_1,
                 data_bits: int=DirectSerial.DATA_BITS_8,
                 read_timeout: NumberType=5,
                 write_timeout: NumberType=5,
                 connect_timeout: Optional[NumberType]=30,
                 connect_retry: bool=True,
                 connect_settle_time: NumberType=3,
                 connect: bool=True):
        

        if mo == MO.DIRECT_SERIAL:
            self.direct_serial = DirectSerial(
                device, device_serial, device_number, device_port, baudrate,
                parity, stop_bits, data_bits, read_timeout, write_timeout,
                connect_timeout, connect_retry, connect_settle_time, connect)
            return

        if mo == MO.DIRECT_MIDDLEBOX:
            self.id = Serial.middlebox_client.initialize(
                None, device, device_serial, device_number, device_port,
                baudrate, parity, stop_bits, data_bits, read_timeout,
                write_timeout, connect_timeout, connect_retry,
                connect_settle_time, connect)
            return

        self.direct_serial = DirectSerial(
            device, device_serial, device_number, device_port, baudrate,
            parity, stop_bits, data_bits, read_timeout, write_timeout,
            connect_timeout, connect_retry, connect_settle_time, connect)
        try: self.id = Serial.middlebox_client.initialize(
                None, device, device_serial, device_number, device_port,
                baudrate, parity, stop_bits, data_bits, read_timeout,
                write_timeout, connect_timeout, connect_retry,
                connect_settle_time, connect)
        except: return
        
    def open_device(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.open_device()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.open_device(self.id)
        response = self.direct_serial.open_device()
        try: Serial.middlebox_client.open_device_trace(self.id, response))
        except: return response

    def connect(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.connect()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.connect(self.id)
        response = self.direct_serial.connect()
        try: Serial.middlebox_client.connect_trace(self.id, response)
        except: return response

    def disconnect(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.disconnect()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.disconnect(self.id)
        response = self.direct_serial.disconnect()
        try: Serial.middlebox_client.disconnect_trace(self.id, response)
        except: return response

    def init_device(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.init_device()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.init_device(self.id)
        response = self.direct_serial.init_device()
        try: Serial.middlebox_client.init_device_trace(self.id, response)
        except: return response

    def set_parameters(self,
                       baudrate: Optional[int]=None,
                       parity: Optional[int]=None,
                       stop_bits: Optional[int]=None,
                       data_bits: Optional[int]=None):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.set_parameters(
            baudrate, parity, stop_bits, data_bits)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.set_parameters(
            None, self.id, baudrate, parity, stop_bits, data_bits)
        response = self.direct_serial.set_parameters(
            baudrate, parity, stop_bits, data_bits)
        try: Serial.middlebox_client.set_parameters(
            response, self.id, baudrate, parity, stop_bits, data_bits)
        except: return response

    def update_timeouts(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.update_timeouts()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.update_timeouts(self.id)
        response = self.direct_serial.update_timeouts()
        try: Serial.middlebox_client.update_timeouts_trace(self.id, response)
        except: return response

    @property
    def info(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.info
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.info(self.id)
        response = self.direct_serial.info
        try: Serial.middlebox_client.info_trace(self.id, response)
        except: return response

    @property
    def serial_number(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.serial_number
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.serial_number(self.id)
        response = self.direct_serial.serial_number
        try: Serial.middlebox_client.serial_number_trace(self.id, response)
        except: return response

    @property
    def in_waiting(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.in_waiting
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.in_waiting(self.id)
        response = self.direct_serial.in_waiting
        try: Serial.middlebox_client.in_waiting_trace(self.id, response)
        except: return response

    @property
    def out_waiting(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.out_waiting
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.out_waiting(self.id)
        response = self.direct_serial.out_waiting
        try: Serial.middlebox_client.out_waiting_trace(self.id, response)
        except: return response

    @property
    def read_timeout(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.read_timeout
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.read_timeout(self.id)
        response = self.direct_serial.read_timeout
        try: Serial.middlebox_client.read_timeout_trace(self.id, response)
        except: return response

    @read_timeout.setter
    def read_timeout(self, value):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.read_timeout(value)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.set_read_timeout(None, self.id, value)
        response = self.direct_serial.read_timeout(value)
        try: Serial.middlebox_client.set_read_timeout_trace(self.id, response)
        except: return response

    @property
    def write_timeout(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.write_timeout
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.write_timeout(self.id)
        response = self.direct_serial.write_timeout
        try: Serial.middlebox_client.write_timeout_trace(self.id, response)
        except: return response

    @write_timeout.setter
    def write_timeout(self, value):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.write_timeout(value)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.set_write_timeout(None, self.id, value)
        response = self.direct_serial.write_timeout(value)
        try: Serial.middlebox_client.set_write_timeout_trace(self.id, response)
        except: return response

    def read(self, num_bytes: int=None, timeout: Optional[NumberType]=None):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.read(num_bytes, timeout)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.read(None, self.id, num_bytes, timeout)
        response = self.direct_serial.read(num_bytes, timeout)
        try: Serial.middlebox_client.read_trace(self.id, response, num_bytes, timeout)
        except: return response

    def read_line(self, line_ending: bytes=b'\r', timeout: Optional[NumberType]=None):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.read_line(num_bytes, timeout)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.read_line(None, self.id, num_bytes, timeout)
        response = self.direct_serial.read_line(num_bytes, timeout)
        try: Serial.middlebox_client.read_line_trace(self.id, response, num_bytes, timeout)
        except: return response

    def write(self, data: Union[bytes, str], timeout: Optional[NumberType]=None):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.write(data, timeout)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.write(None, self.id, data, timeout)
        response = self.direct_serial.write(data, timeout)
        try: Serial.middlebox_client.write_trace(self.id, response, data, timeout)
        except: return response

    def request(self, data: bytes, timeout: Optional[NumberType]=None, line_ending: bytes=b'\r'):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.request(data, timeout, line_ending)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.request(None, self.id, data, timeout, line_ending)
        response = self.direct_serial.request(data, timeout, line_ending)
        try: Serial.middlebox_client.request_trace(self.id, response, data, timeout, line_ending)
        except: return response

    def flush(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.flush()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.flush(self.id)
        response = self.direct_serial.flush()
        try: Serial.middlebox_client.flush_trace(self.id, response)
        except: return response

    def reset_input_buffer(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.reset_input_buffer()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.reset_input_buffer(self.id)
        response = self.direct_serial.reset_input_buffer()
        try: Serial.middlebox_client.reset_input_buffer_trace(self.id, response)
        except: return response

    def reset_output_buffer(self):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.reset_output_buffer()
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.reset_output_buffer(self.id)
        response = self.direct_serial.reset_output_buffer()
        try: Serial.middlebox_client.reset_output_buffer_trace(self.id, response)
        except: return response

    def set_bit_mode(self, mask: int, enable: bool):
        if mo == MO.DIRECT_SERIAL: return self.direct_serial.set_bit_mode(mask, enable)
        if mo == MO.DIRECT_MIDDLEBOX: return Serial.middlebox_client.set_bit_mode(None, self.id, mask, enable)
        response = self.direct_serial.set_bit_mode(mask, enable)
        try: Serial.middlebox_client.set_bit_mode_trace(self.id, response, mask, enable)
        except: return response
