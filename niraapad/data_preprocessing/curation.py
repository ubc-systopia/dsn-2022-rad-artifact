import pickle
import os
import inspect
import json
from pymongo import MongoClient
from itertools import repeat
from datetime import datetime


from itertools import repeat
from niraapad.backends import DirectUR3Arm
from niraapad.backends import DirectFtdiDevice, DirectPySerialDevice, DirectArduinoStepper
import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc
from niraapad.shared.tracing import Tracer
from niraapad.data_preprocessing.commands import magneticstirrer_commands

# Path to this file test_niraapad.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))


class Curator:

    def __init__(self, trace_path=niraapad_path+"\\niraapad\\traces", json_path=niraapad_path+"\\niraapad\\logs", database="heinLabTracingData", collection="commandTraces"):
        self.trace_path = trace_path
        self.json_path = json_path
        self.database = database
        self.collection = collection
        self.backend_instance_id_magstr = []

    
    def convert_to_commands(self, method_name, field, value, backend_instance_id):
        commands = {}

        #Return magnetic stirrer commands
        if  backend_instance_id in self.backend_instance_id_magstr:
            magstr = magneticstirrer_commands()
            if method_name == "write":
                commands = magstr.write_ika(value, commands)  
            elif method_name == "read":
                commands = magstr.read_ika(value,commands)
        else:
            commands[field] = str(value)

        return commands

    def convert_args(self, trace_msg_type, trace_msg, args, kwargs, backend_instance_id):
        # Get the argspec of the Initialization and other functions
        if trace_msg_type != "InitializeTraceMsg":
            argspecs = inspect.getfullargspec(eval(trace_msg.req.backend_type + "." + trace_msg.req.method_name))
        else:
            argspecs = inspect.getfullargspec(eval(trace_msg.req.backend_type + ".__init__"))

        arg_val = {}
        check = 'o'

        # Get the default values of the function
        if argspecs.defaults == None:
            defaults = argspecs.defaults
        elif len(argspecs.args) != len(argspecs.defaults):
            empty_spaces = tuple(repeat(None, len(argspecs.args)-len(argspecs.defaults)))
            defaults = empty_spaces + argspecs.defaults
        else:
            defaults = argspecs.defaults

        #Adding the kwargs of the function to the dictionary arg_val
        for val in kwargs:
            if isinstance(kwargs[val], bytes):
                if val == "data":
                    arg_val[val] = self.convert_to_commands(trace_msg.req.method_name, val, kwargs[val], backend_instance_id)
                else:
                    arg_val[val] = kwargs[val].decode()
            else:
                arg_val[val] = str(kwargs[val])

        #Adding the args and the default values to the dictionary arg_val
        i = 1
        for arg in argspecs.args:
            if arg == "self":
                continue
            else:
                if check == 'o':
                    check= 'a'
                    for val in args:
                        if isinstance(val, bytes):
                            if (arg == "data"):
                               arg_val[arg] = self.convert_to_commands(trace_msg.req.method_name, arg, val, backend_instance_id)
                            else:
                                arg_val[arg] = val.decode()
                        else:
                            arg_val[arg] = str(val)
                elif check == 'a':
                    if arg not in arg_val.keys():
                        try:
                            arg_val[arg] = str(defaults[i])
                        except:
                            pass
            i = i + 1

        return arg_val
        


    def convert_to_json(self, parsing_file):
        print(parsing_file)
        traces = {}
        traces['Traces'] = []

        #Parse the tracing file
        for timestamp, trace_msg_type, trace_msg in Tracer.parse_file(parsing_file):
            trace_msg_parse = {}


            
            if str(trace_msg) != '':
                #Seperate the response and request
                for field, sub_fields in trace_msg.ListFields():
                    msg_sub_field = {}

                    #Convert response and request in json format
                    for sub_field, value in sub_fields.ListFields():
                        #Merge args and kwargs, conversion to json format
                        if str(sub_field.name) == "args":
                            args = pickle.loads(value)
                        elif str(sub_field.name) == "kwargs":
                            msg_sub_field["args"] = self.convert_args(trace_msg_type, trace_msg, args, pickle.loads(value), trace_msg.req.backend_instance_id)
                        #Pickle if the value is in bytes format
                        elif isinstance(value, bytes):
                            #Checking for read commands for the modules
                            try:
                                if isinstance(pickle.loads(value), bytes) and pickle.loads(value)!= None:
                                    msg_sub_field[str(sub_field.name)] = self.convert_to_commands(trace_msg.req.method_name, sub_field.name, pickle.loads(value), trace_msg.req.backend_instance_id)                            
                                else:
                                    msg_sub_field[str(sub_field.name)] = str(pickle.loads(value))
                            except:
                                msg_sub_field[str(sub_field.name)] = str(value)
                        else:
                            msg_sub_field[str(sub_field.name)] = value


                    #Pass the parsed trace message
                    trace_msg_parse[str(field.name)] = msg_sub_field

            if trace_msg_type == "InitializeTraceMsg":
                stacktrace = trace_msg_parse['req']['stacktrace']
                if "magnetic_stirrer.py" in stacktrace:
                    self.backend_instance_id_magstr.append(trace_msg_parse['req']['backend_instance_id'])




            #Creating the dictionary of traces
            traces['Traces'].append({
                    '_id' : timestamp,
                    'Trace Message Type' : trace_msg_type,
                    'Trace Message' : trace_msg_parse
                })
        

        return traces

    def write_to_json_file(self, traces, filename):
        #Dump json to json file
        with open(filename.strip(".log") + ".json", "w") as outfile:
            json.dump(traces,outfile)   

    def dumping_in_db(self, json_path):
        #Fetching the json file
        with open(json_path, "r") as jsonfile:
            traces = json.load(jsonfile)
          
        #Initilazing the database and collection
        client = MongoClient("localhost", 27017)
        db = client[self.database]
        collectionTraces = db[self.collection]

        #Dumping the traces to the database
        try:
            collectionTraces.insert_many(traces['Traces'])
        except Exception as e:
            print("Exception:", e)

    def main_process(self):
        #Get the list of tracing files
        tracing_files = os.listdir(self.trace_path)

        #Convert all files to json format and write it to the file
        for file in tracing_files:
            parsing_file = self.trace_path + "\\" + file
            traces = self.convert_to_json(parsing_file)      
            self.write_to_json_file(traces, self.json_path + "\\" + file) 
        
        #Get the list of json files
        #json_files = os.listdir(self.json_path)

        #Dump it in db
        #for file in json_files:
        #    json_log_file = self.json_path + "\\" + file
        #    self.dumping_in_db(json_log_file)

if __name__ == "__main__":
    curation = Curator()
    curation.main_process()









    
