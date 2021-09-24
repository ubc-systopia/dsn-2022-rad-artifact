import os
import sys

import niraapad.shared.utils as utils
from niraapad.lab_computer.niraapad_client import NiraapadClient


class AttributeMeta(type):

    def __getattribute__(cls, key):
        """
        This function overrides the object.__getattribute__ method and is used
        trap and appropriately handle all read accesses to class variables.
        """

        try:
            return type.__getattribute__(cls, key)
        except AttributeError:
            niraapad_backend_type = type.__getattribute__(
                cls, "niraapad_backend_type")
            return NiraapadClient.static_getter(niraapad_backend_type, key)

    def __setattr__(cls, key, value):
        """
        This function overrides the type.__setattr__ method and is used to
        trap and appropriately handle all write accesses to class variables.
        """

        niraapad_backend_type = type.__getattribute__(cls,
                                                      "niraapad_backend_type")
        NiraapadClient.static_setter(niraapad_backend_type, key, value)


# Ignoring class ftdi_serial.Serial because we have
# decided to virtualize the Device classes instead,
# which actually are closer to the network layer

# class VirtualSerial(NiraapadClient, metaclass=AttributeMeta):
#     """
#     This class is just a facade. It's objective is to provide the same
#     interface to all Hein Lab experiment scripts as the erstwhile "class
#     Serial". In addition, the class maintains three operation modes as
#     summarized above along in "class MO". In order to do so, this class simply
#     forwards each function call to the respective function call in the
#     respective origianl Serial class object (class objects are not involved in
#     the case of static functions), or to the respective function call in the
#     global object of type "class NiraapadClientHelper" (which in turn invokes
#     an RPC to the middlebox), or both.
#     """

#     niraapad_backend_type = utils.BACKENDS.SERIAL
#     niraapad_access_variable = ""

#     @staticmethod
#     def list_devices(*args, **kwargs):
#         return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

#     @staticmethod
#     def list_device_ports(*args, **kwargs):
#         return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

#     @classmethod
#     def list_device_serials(cls, *args, **kwargs):
#         return NiraapadClient.static_method(VirtualSerial.niraapad_backend_type, *args, **kwargs)

#     def __init__(self, *args, **kwargs):
#         return self.initialize(*args, **kwargs)

#     def open_device(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def connect(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def disconnect(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def init_device(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def set_parameters(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def update_timeouts(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def read(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def read_line(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def write(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def request(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def flush(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def reset_input_buffer(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def reset_output_buffer(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def set_bit_mode(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)


class VirtualDevice(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Device". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original Device class object (class objects are not involved
    in the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.DEVICE
    niraapad_access_variable = ""  #"device"

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def add_write_handler(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def purge(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_baud_rate(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_input_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_output_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read_all(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def enable_write_log(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_write_log(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear_write_log(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_bit_mode(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


# Among all the Device subclasses,
# supporting classes FtdiDevice and PySerialDevice,
# but ignoring class ftdi_serial.MockDevice,
# because it is not supported in ftdi-serial v0.1.9

# class VirtualMockDevice(VirtualDevice, metaclass=AttributeMeta):
#     """
#     This class is just a facade. It's objective is to provide the same
#     interface to all Hein Lab experiment scripts as the erstwhile "class
#     MockDevice". In addition, the class maintains three operation modes as
#     summarized above along in "class MO". In order to do so, this class simply
#     forwards each function call to the respective function call in the
#     respective original MockDevice class object (class objects are not involved in
#     the case of static functions), or to the respective function call in the
#     global object of type "class NiraapadClientHelper" (which in turn invokes
#     an RPC to the middlebox), or both.
#     """

#     niraapad_backend_type = utils.BACKENDS.MOCK_DEVICE
#     niraapad_access_variable = "" #"device"

#     def __init__(self, *args, **kwargs):
#         return self.initialize(*args, **kwargs)

#     def close(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def clear(self, *args, **kwargs)
#         return self.generic_method(*args, **kwargs)

#     def get_input_size(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def write(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)

#     def read(self, *args, **kwargs):
#         return self.generic_method(*args, **kwargs)


class VirtualFtdiDevice(VirtualDevice, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    FtdiDevice". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original FtdiDevice class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.FTDI_DEVICE
    niraapad_access_variable = ""  #"device"

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_baud_rate(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_input_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_output_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_bit_mode(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualPySerialDevice(VirtualDevice, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    PySerialDevice". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original PySerialDevice class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.PY_SERIAL_DEVICE
    niraapad_access_variable = ""  #"device"

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_baud_rate(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_timeouts(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_parameters(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_input_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def get_output_size(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualRobotArm(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    RobotArm". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original RobotArm class object (class objects are not involved
    in the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.ROBOT_ARM
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def pause(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def resume(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def emergency_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear_faults(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def home(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_tool(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_to_location(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_tool_to_location(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_to_locations(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_tool_to_locations(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_joints(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_joint(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_twist(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_twist_to(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for_gripper_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def open_gripper(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def close_gripper(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualUR3Arm(VirtualRobotArm, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    UR3Arm". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original UR3Arm class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.UR3_ARM
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def close(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def emergency_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_to_location(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_joints(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_circular(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for_gripper_stop(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def open_gripper(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualKortexConnection(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    KortexConnection". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original KortexConnection class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.KORTEX_CONNECTION
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def disconnect(self):
        self.client.Unsubscribe(self.subscription)

    def dispatch_notification(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def add_notification_listener(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def remove_notification_listener(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for_notification(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for_action_end(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def execute_action(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def execute_gripper_command(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def execute_existing_action(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualArduinoStepper(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    ArduinoStepper". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original ArduinoStepper class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.ARDUINO_STEPPER
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def _connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def check_value(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def calc_travel_time(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def send_string(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def rotate_steps(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def rotate_revolution(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def home(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def home_direction(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def current_position(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def target_position(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def busy(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def stop_motor(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def ping_accel_regsiter(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def ping_comp_register(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualBalance(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Balance". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original Balance class object (class objects are not involved
    in the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.BALANCE
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def __del__(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def _response_monitor(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def _handle_response(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    @staticmethod
    def package_and_encode(*args, **kwargs):
        return NiraapadClient.static_method(
            VirtualBalance.niraapad_backend_type, *args, **kwargs)

    @staticmethod
    def _string_command_parse(*args, **kwargs):
        return NiraapadClient.static_method(
            VirtualBalance.niraapad_backend_type, *args, **kwargs)

    @staticmethod
    def _string_response_parse(*args, **kwargs):
        return NiraapadClient.static_method(
            VirtualBalance.niraapad_backend_type, *args, **kwargs)

    def _send_command(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def send_and_retrieve_response(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def _retrieve_unchanging(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def _wait_for_response_to_command(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def retrieve_response(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def tare(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def clear_tare_value(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def tare_immediately(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def zero(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def zero_immediately(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def cancel_operations(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def write_text_on_screen(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualQuantos(VirtualBalance, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    Quantos". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original Quantos class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.QUANTOS
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    @staticmethod
    def _string_command_parse(*args, **kwargs):
        return NiraapadClient.static_method(
            VirtualQuantos.niraapad_backend_type, *args, **kwargs)

    @staticmethod
    def _string_response_parse(*args, **kwargs):
        return NiraapadClient.static_method(
            VirtualQuantos.niraapad_backend_type, *args, **kwargs)

    def _handle_response(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def _warn_not_set(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def _send_command(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def send_and_wait_for_completion(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def set_pan_empty(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def label_sample_data(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def protocol_sample_data(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def lock_dosing_pin_position(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def unlock_dosing_pin_position(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def start_dosing(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def stop_dosing(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def cut_label(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def wait_for(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def force_unlock(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualArduinoAugment(NiraapadClient, metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    ArduinoAugment". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original ArduinoAugment class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.ARDUINO_AUGMENT
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)

    def set_home_direction(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def home_z_stage(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)

    def move_z_stage(self, *args, **kwargs):
        return self.generic_method(*args, **kwargs)


class VirtualArduinoAugmentedQuantos(VirtualQuantos,
                                     VirtualArduinoAugment,
                                     metaclass=AttributeMeta):
    """
    This class is just a facade. It's objective is to provide the same
    interface to all Hein Lab experiment scripts as the erstwhile "class
    ArduinoAugmentedQuantos". In addition, the class maintains three operation modes as
    summarized above along in "class MO". In order to do so, this class simply
    forwards each function call to the respective function call in the
    respective original ArduinoAugmentedQuantos class object (class objects are not involved in
    the case of static functions), or to the respective function call in the
    global object of type "class NiraapadClientHelper" (which in turn invokes
    an RPC to the middlebox), or both.
    """

    niraapad_backend_type = utils.BACKENDS.ARDUINO_AUGMENTED_QUANTOS
    niraapad_access_variable = ""

    def __init__(self, *args, **kwargs):
        return self.initialize(*args, **kwargs)


# ===== THESE ARE IMPORTANT FOR MONKEY PATCHING =====
# Ignoring class ftdi_serial.Serial because we have
# decided to virtualize the Device classes instead,
# which actually are closer to the network layer
# DirectSerial = ftdi_serial.Serial
# ftdi_serial.Serial = VirtualSerial

# # Among all the Device subclasses,
# # supporting classes FtdiDevice and PySerialDevice,
# # but ignoring class ftdi_serial.MockDevice,
# # because it is not supported in ftdi-serial v0.1.9
# DirectMockDevice = ftdi_serial.MockDevice
# ftdi_serial.MockDevice = VirtualMockDevice

import ftdi_serial

DirectFtdiDevice = ftdi_serial.FtdiDevice
ftdi_serial.FtdiDevice = VirtualFtdiDevice

DirectPySerialDevice = ftdi_serial.PySerialDevice
ftdi_serial.PySerialDevice = VirtualPySerialDevice

# The UR3Arm does not directly rely on the Device
# classes (i.e., serial communication) but instead
# communicates with the lab computer over LAN

from hein_robots.universal_robots import ur3

DirectUR3Arm = ur3.UR3Arm
ur3.UR3Arm = VirtualUR3Arm

# The KinovaGen3Arm relies on the KortexConnection class,
# which in turn relies on a third-party kortex_api project.
# We therefore virtualize KortexConnection in our project.

from hein_robots.kinova import kortex

DirectKortexConnection = kortex.KortexConnection
kortex.KortexConnection = VirtualKortexConnection

# The ArduinoStepper class is controlled by serial,
# but it uses the third-party (Python's) serial.Serial
# as opposed to our ftdi_serial.Serial. Therefore, we
# also virtualize this class.

# from arduino_stepper import api

# DirectArduinoStepper = api.ArduinoStepper
# api.ArduinoStepper = VirtualArduinoStepper

# The ArduinoAugmentedQuantos class extends the ArduinoAugment
# and the Quantos class. The Quantos class uses a TCP
# connection. We thus virtualize this class.

from mtbalance import arduino

DirectArduinoAugmentedQuantos = arduino.ArduinoAugmentedQuantos
arduino.ArduinoAugmentedQuantos = VirtualArduinoAugmentedQuantos
# ===================================================
