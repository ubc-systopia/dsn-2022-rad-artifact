import inspect

import niraapad.shared.utils as utils

from niraapad.lab_computer.niraapad_client import NiraapadClient

class Serial(NiraapadClient):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Serial". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective origianl Serial class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """
    
    backend_type = utils.BACKENDS.SERIAL

    @staticmethod
    def list_devices(*args, **kwargs):
        return NiraapadClient.static_method(Serial.backend_type, *args, **kwargs)

    @staticmethod
    def list_device_ports(*args, **kwargs):
        return NiraapadClient.static_method(Serial.backend_type, *args, **kwargs)

    @classmethod
    def list_device_serials(cls, *args, **kwargs):
        return NiraapadClient.static_method(Serial.backend_type, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def open_device(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def init_device(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def update_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    @property
    def info(self):
        return self.generic_getter()

    @property
    def serial_number(self):
        return self.generic_getter()

    @property
    def in_waiting(self):
        return self.generic_getter()

    @property
    def out_waiting(self):
        return self.generic_getter()

    @property
    def read_timeout(self):
        return self.generic_getter()

    @read_timeout.setter
    def read_timeout(self, value):
        self.generic_setter(value)

    @property
    def write_timeout(self):
        return self.generic_getter()

    @write_timeout.setter
    def write_timeout(self, value):
        self.generic_setter(value)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read_line(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def request(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def flush(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset_input_buffer(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset_output_buffer(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_bit_mode(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)
