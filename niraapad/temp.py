import inspect
from typing import Any, Union, List, Optional, Callable

class Temp:
  def trial(self,
            device_serial: Optional[str]=None,
            device_number: Optional[int]=None,
            baudrate: int=115200,
            connect_timeout: Optional[float]=30,
            connect_retry: bool=True):
    print("1", str(device_serial))
    print("2", str(device_number))
    print("3", str(baudrate))
    print("4", str(connect_timeout))
    print("5", str(connect_retry))

def temp_trial(*args, **kwargs):
  print("==========")
  #print(args)
  #print(kwargs)
  print(inspect.getfullargspec(Temp.trial))

  #if len(args) > 0: kwargs['device_serial'] = args[0]
  #if len(args) > 1: kwargs['device_number'] = args[1]
  #if len(args) > 2: kwargs['baudrate'] = args[2]
  #if len(args) > 3: kwargs['connect_timeout'] = args[3]
  #if len(args) > 4: kwargs['connect_retry'] = args[4]

  #print(kwargs)

  temp = Temp()
  method_call = "temp.trial("
  for i in range(0, len(args)):
      #if method_call[-1] != "(":
      #  method_call += ", "
      method_call += "args[" + str(i) + "], "
  for argname in inspect.getfullargspec(Temp.trial).args:
    if argname == "self":
      continue
    if argname in kwargs:
      #if method_call[-1] != "(":
      #  method_call += ", "
      method_call += argname + "=kwargs['" + argname + "'], "
  method_call += ")"
  print("Calling", method_call)
  eval(method_call)
  #temp.trial(kwargs['device_serial'],
  #           kwargs['device_number'],
  #           kwargs['baudrate'],
  #           kwargs['connect_timeout'],
  #           kwargs['connect_retry'])
  #temp = Temp(args, kwargs)
  #temp = getattr(Temp, 'trial')(args, kwargs)

temp_trial()
temp_trial("FTP")
temp_trial("FTP", 5)
temp_trial(connect_timeout=15)
temp_trial(device_number=5, connect_timeout=15)
temp_trial("FTP", connect_timeout=15)
