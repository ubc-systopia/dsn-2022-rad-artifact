from typing import Any, Union, List, Optional, Callable
import middlebox_client

SerialDeviceType = Union[str, int, 'Device']
NumberType = Union[float, int]

middlebox_client = MiddleboxClient()

class Serial:

    PARITY_NONE = 0
    PARITY_ODD = 1
    PARITY_EVEN = 2
    STOP_BITS_1 = 0
    STOP_BITS_2 = 2
    DATA_BITS_7 = 7
    DATA_BITS_8 = 8

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
        self.id = middlebox_client.initialize(device,
                                              device_serial,
                                              device_number,
                                              device_port,
                                              baudrate,
                                              parity,
                                              stop_bits,
                                              data_bits,
                                              read_timeout,
                                              write_timeout,
                                              connect_timeout,
                                              connect_retry,
                                              connect_settle_time,
                                              connect)

    def open_device(self):
        """ This interface needn't be exposed on the client side """
        assert False

    def connect(self):
        """
        Connect to the serial device if a connection hasn't been made (this is not needed in most cases)
        """
        middlebox_client.connect(self.id)

    def disconnect(self):
        """
        Disconnect the serial device
        """
        middlebox_client.disconnect(self.id)

    def init_device(self):
        """ This interface needn't be exposed on the client side """
        assert False

    def set_parameters(self, baudrate: Optional[int]=None, parity: Optional[int]=None, stop_bits: Optional[int]=None, data_bits: Optional[int]=None):
        """
        Change the serial connection parameters for the serial device
        """
        middlebox_client.set_parameters(self.id, baudrate, parity, stop_bits, data_bits)

    def update_timeouts(self):
        """
        Change the timeout parameters for the serial device
        """
        middlebox_client.update_timeouts(self.id)

    @property
    def info(self) -> SerialDeviceInfo:
        """
        Get info about the connected serial device

        :return: SerialDeviceInfo instance
        """
        return middlebox_client.info(self.id)

    @property
    def serial_number(self)-> str:
        """
        Get the serial number for the conneted device, if available

        :return: serial number string
        """
        return middlebox_client.serial_number(self.id)

    @property
    def in_waiting(self) -> int:
        """ This interface needn't be exposed on the client side """
        assert False

    @property
    def out_waiting(self) -> int:
        """ This interface needn't be exposed on the client side """
        assert False

    @property
    def read_timeout(self):
        """ This interface needn't be exposed on the client side """
        assert False

    @read_timeout.setter
    def read_timeout(self, value):
        """ This interface needn't be exposed on the client side """
        assert False

    @property
    def write_timeout(self):
        """ This interface needn't be exposed on the client side """
        assert False

    @write_timeout.setter
    def write_timeout(self, value):
        """ This interface needn't be exposed on the client side """
        assert False

    def read(self, num_bytes: int=None, timeout: Optional[NumberType]=None) -> bytes:
        """
        Read bytes from the serial device

        :param num_bytes: [Optional] number of bytes to read, defaults to reading the entire input buffer if not given (will wait for at least 1 byte if buffer empty)
        :param timeout: [Optional] read timeout to use while reading, will be reset to default afterwards

        :return: data bytes
        """
        return middlebox_client.read(self.id, num_bytes, timeout)

    def read_line(self, line_ending: bytes=b'\r', timeout: Optional[NumberType]=None) -> bytes:
        """
        Read a "line" of data from the serial device until the given line ending is found

        :param line_ending: the line ending byte(s) to look for, defaults to ``b'\\r'``
        :param timeout: the timeout to use while reading data, will be reset to default afterwards
        :return: bytes of data
        """
        return middlebox_client.read_line(self.id, line_ending, timeout)


    def write(self, data: Union[bytes, str], timeout: Optional[NumberType]=None) -> int:
        """
        Write the given data to the serial device

        :param data: a string or bytes of data to write
        :param timeout: [Optional] timeout to use when writing data, will be reset to default

        :return: number of bytes written
        """
        return middlebox_client.write(self.id, data, timeout)

    def request(self, data: bytes, timeout: Optional[NumberType]=None, line_ending: bytes=b'\r'):
        """
        Perform a "request", which writes the given data and then reads the "response" from the serial device until the
        given line ending is found

        :param data: request data to write
        :param timeout: [Optional] read timeout to use when reading response
        :param line_ending: [Optional] line ending byte(s) to look for in response, defaults to ``b'\\r'``
        :return: bytes of response data
        """
        return middlebox_client.request(self.id, data, timeout, line_ending)

    def flush(self):
        """ This interface needn't be exposed on the client side """
        assert False

    def reset_input_buffer(self):
        """ This interface needn't be exposed on the client side """
        assert False

    def reset_output_buffer(self):
        """ This interface needn't be exposed on the client side """
        assert False

    def set_bit_mode(self, mask: int, enable: bool):
        """ This interface needn't be exposed on the client side """
        assert False
