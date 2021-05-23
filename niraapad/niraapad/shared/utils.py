from enum import Enum
import inspect

class MO(Enum):
    DIRECT_SERIAL = 1
    DIRECT_MIDDLEBOX = 2
    DIRECT_SERIAL_WITH_MIDDLEBOX_TRACING = 3

def EmptyStringIfNone(data):
  if data == None: return ""
  else: return data

def NoneIfEmptyString(data):
  if data == "": return None
  else: return data

func_name = lambda: inspect.stack()[1].function
caller_func_name = lambda: inspect.stack()[2].function
max_func_name_len = 100
