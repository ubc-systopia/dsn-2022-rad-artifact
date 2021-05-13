from typing import Any, Union, List, Optional, Callable

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

    def __str__(self):
        return "SerialDeviceInfo: index = %s, device serial number = %s, port = %s, description = %s" % \
            (str(self.index), str(self.serial), str(self.port), str(self.description))
