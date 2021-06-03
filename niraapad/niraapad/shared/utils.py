from enum import Enum
import inspect

func_name = lambda: inspect.stack()[1].function
caller_func_name = lambda: inspect.stack()[2].function
max_func_name_len = 100

def EmptyStringIfNone(data):
  if data == None: return ""
  else: return data

def NoneIfEmptyString(data):
  if data == "": return None
  else: return data

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

class MO(Enum):
    DIRECT_SERIAL = 1
    DIRECT_MIDDLEBOX = 2
    DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING = 3
