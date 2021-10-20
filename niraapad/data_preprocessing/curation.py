import pickle
import os
import inspect
import json
from pymongo import MongoClient
from itertools import repeat
from datetime import datetime
import csv

from itertools import repeat
import niraapad.backends
from niraapad.lab_computer.niraapad_client import NiraapadClient
from niraapad.backends import DirectUR3Arm
from niraapad.backends import DirectFtdiDevice, DirectPySerialDevice
from niraapad.backends import DirectArduinoAugmentedQuantos
import niraapad.protos.niraapad_pb2 as niraapad_pb2
import niraapad.protos.niraapad_pb2_grpc as niraapad_pb2_grpc
from niraapad.shared.tracing import Tracer
from niraapad.data_preprocessing.commands import magneticstirrer_commands, tecancavro_commands, controller_commands

# Path to this file test_niraapad.py
file_path = os.path.dirname(os.path.abspath(__file__))

# Path to the cps-security-code (aka project niraapad) git repo
niraapad_path = os.path.dirname(os.path.dirname(file_path))


class Curator:

    def __init__(self, trace_path=niraapad_path+"\\niraapad\\traces", json_path=niraapad_path+"\\niraapad\\logs", csv_path=niraapad_path+"\\niraapad\\csv", database="heinLabTracingData", collection="commandTraces"):
        self.trace_path = trace_path
        self.json_path = json_path
        self.csv_path = csv_path
        self.database = database
        self.collection = collection
        self.backend_instance_id_magstr = []
        self.backend_instance_id_cavro = []
        self.backend_instance_id_c9 = []
        self.backend_instance_id_arduino = []
        self.backend_instance_id_ur = []
    
    def convert_to_commands(self, method_name, field, value, backend_instance_id):
        commands = {}
        
        #Return magnetic stirrer commands
        if  backend_instance_id in self.backend_instance_id_magstr:
            magstr = magneticstirrer_commands()
            if method_name == "write":
                commands = magstr.write_ika(value, commands)  
            elif method_name == "read":
                commands = magstr.read_ika(value,commands)
        elif backend_instance_id in self.backend_instance_id_c9:
            #print(value)
            c9 = controller_commands()
            if method_name == "write":
                commands = c9.write_centrifuge(value, commands)
            elif method_name == "read":
                commands = c9.read_line_centrifuge(value, commands)
        elif backend_instance_id in self.backend_instance_id_cavro:
            t_cavro = tecancavro_commands()
            if method_name == "write":
                commands = t_cavro.write_cavro(value, commands)  
            elif method_name == "read":
                commands = t_cavro.read_cavro(value,commands)
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
                        #if (sub_field.name == "time_profiles"):
                           # print(type(value))
                           # print(json.loads(str(value).replace("\n",",\n")))
                        #Merge args and kwargs, conversion to json format
                        if str(sub_field.name) == "args":
                            args = pickle.loads(value)
                        elif str(sub_field.name) == "kwargs":
                            msg_sub_field["args"] = self.convert_args(trace_msg_type, trace_msg, args, pickle.loads(value), trace_msg.req.backend_instance_id)
                        #Time Profile conversion to json format
                        elif str(sub_field.name) == "time_profiles":
                            time_profile = {}
                            #print(trace_msg.req.time_profiles.listFields())
                            for val in value:
                                time_profile['id'] = val.id
                                time_profile['arrival_time'] = val.arrival_time
                                time_profile['departure_time'] = val.departure_time
                            msg_sub_field["time_profile"] = time_profile
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
                elif "controller.py" in stacktrace:
                    self.backend_instance_id_c9.append(trace_msg_parse['req']['backend_instance_id'])
                elif "controller.py" not in stacktrace and trace_msg_parse['req']['backend_type'] == "DirectFtdiDevice":
                    self.backend_instance_id_cavro.append(trace_msg_parse['req']['backend_instance_id'])
                else:
                    self.backend_instance_id_arduino.append(trace_msg_parse['req']['backend_instance_id'])

            
            #print(trace_msg_parse)
            

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


    def dumping_in_csv(self, json_path, file):
        #Fetching the json file
        with open(json_path, "r") as jsonfile:
            traces = json.load(jsonfile)
        
        header = ["Timestamp", "Module", "Method_Name", "Arguments", "Responses", "Exceptions"]
        
        #Opening csv file
        with open(self.csv_path + "\\" + file.strip(".json") + ".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)

            for trace in traces['Traces']:
                module = ""
                if trace['Trace Message Type'] == "InitializeTraceMsg":
                    if "magnetic_stirrer.py" in trace['Trace Message']['req']['stacktrace']:
                        self.backend_instance_id_magstr.append(trace['Trace Message']['req']['backend_instance_id'])
                        writer.writerow([trace['_id'], "Magnetic Stirrer", "_init_", str(trace['Trace Message']['req']['args']).replace("{", "").replace("}", "").replace("{","").replace("'","").strip(','), None, trace['Trace Message']['resp']['exception']])
                    elif "controller.py" in trace["Trace Message"]["req"]["stacktrace"]:
                        self.backend_instance_id_c9.append(trace['Trace Message']['req']['backend_instance_id'])
                        writer.writerow([trace['_id'], "N9", "_init_", str(trace['Trace Message']['req']['args']).replace("{", "").replace("}", "").replace("'","").strip(','), None, trace['Trace Message']['resp']['exception']])
                    elif "controller.py" not in trace['Trace Message']["req"]["stacktrace"] and trace["Trace Message"]["req"]["backend_type"] == "DirectFtdiDevice":
                        self.backend_instance_id_cavro.append(trace['Trace Message']['req']['backend_instance_id'])
                        writer.writerow([trace['_id'], "Tecan Cavro", "_init_", str(trace['Trace Message']['req']['args']).replace("{", "").replace("}", "").replace("'","").strip(','), None, trace['Trace Message']['resp']['exception']])
                    else:
                        module = trace['Trace Message']['req']['backend_type'].replace("Direct","")
                        if module == "UR3Arm":
                            self.backend_instance_id_ur.append(trace['Trace Message']['req']['backend_instance_id'])
                        elif module == "ArduinoAugmentedQuantos":
                            self.backend_instance_id_arduino.append(trace['Trace Message']['req']['backend_instance_id'])
                        writer.writerow([trace['_id'], module, "_init_", str(trace['Trace Message']['req']['args']).replace("{", "").replace("}", "").replace("'","").strip(','), None, trace['Trace Message']['resp']['exception']])
            
                elif trace['Trace Message Type'] == "GenericMethodTraceMsg" or trace['Trace Message Type'] == "GenericSetterTraceMsg":
                    if trace['Trace Message']['req']['backend_instance_id'] in self.backend_instance_id_magstr:
                            if 'args' in trace['Trace Message']['req']['args'].keys() and trace['Trace Message']['req']['args']['command_name']:
                                writer.writerow([trace['_id'], "Magnetic Stirrer", str(trace['Trace Message']['req']['args']['command_name']), trace['Trace Message']['req']['args']['value'].replace("{", "").replace("}", "").replace("'","").strip(','), trace['Trace Message']['resp']['resp'], trace['Trace Message']['resp']['exception']])
                        
                    elif trace['Trace Message']['req']['backend_instance_id'] in self.backend_instance_id_c9:
                        
                            if "data" in trace['Trace Message']['req']['args'].keys() and trace['Trace Message']['req']['args']['data']['command_name']:
                                
                                if "args" in trace['Trace Message']['req']['args']['data'].keys():
                                    writer.writerow([trace['_id'], "N9", trace['Trace Message']['req']['args']['data']['command_name'], str(str(trace['Trace Message']['req']['args']['data']['args']).replace("}","").replace("{","").replace("'","") + "," + str(trace['Trace Message']['req']['args']['data']['flags']).replace("{", "").replace("}", "").replace("'","")).strip(','), trace['Trace Message']['resp']['resp'], trace['Trace Message']['resp']['exception']])
                                else:

                                    writer.writerow([trace['_id'], "N9", trace['Trace Message']['req']['args']['data']['command_name'], None, trace['Trace Message']['resp']['resp'], trace['Trace Message']['resp']['exception']])
                    elif trace['Trace Message']['req']['backend_instance_id'] in self.backend_instance_id_cavro:
                            if 'data' in trace['Trace Message']['req']['args'].keys() and 'command_name_0' in trace['Trace Message']['req']['args']['data'].keys() and trace['Trace Message']['req']['args']['data']['command_name_0']:
                                
                                commands_values = list(trace['Trace Message']['req']['args']['data'].keys())
                                i = 0
                                while ( i < len(commands_values)):
            
                                    if i+1 < len(trace['Trace Message']['req']['args']['data'].keys()) and "command" not in commands_values[i+1]:
        
                                        writer.writerow([trace['_id'], "Tecan Cavro", trace['Trace Message']['req']['args']['data'][commands_values[i]], str(commands_values[i+1] +  ":" + str(trace['Trace Message']['req']['args']['data'][commands_values[i+1]])), trace['Trace Message']['resp']['resp'], trace['Trace Message']['resp']['exception']])
                                        i = i + 2
                                    else:  
                                        writer.writerow([trace['_id'], "Tecan Cavro", trace['Trace Message']['req']['args']['data'][commands_values[i]], None, trace['Trace Message']['resp']['resp'], trace['Trace Message']['resp']['exception']])
                                        i = i + 1
                    else:
                        if trace['Trace Message']['req']['backend_instance_id'] in self.backend_instance_id_ur:
                            writer.writerow([trace['_id'], "UR3Arm", trace['Trace Message']['req']['method_name'], str(trace['Trace Message']['req']['args']).replace("{", "").replace("}", "").replace("'","").strip(','), trace['Trace Message']['resp']['resp'],trace['Trace Message']['resp']['exception']])
                        elif trace['Trace Message']['req']['backend_instance_id'] in self.backend_instance_id_arduino:
                            try: 
                                writer.writerow([trace['_id'], "ArduinoAugmentedQuantos", trace['Trace Message']['req']['method_name'], str(trace['Trace Message']['req']['args']).replace("{", "").replace("}", "").replace("'","").strip(','), trace['Trace Message']['resp']['resp'],trace['Trace Message']['resp']['exception']])
                            except:
                                writer.writerow([trace['_id'], "ArduinoAugmentedQuantos", trace['Trace Message']['req']['property_name'], str(trace['Trace Message']['req']['value']).replace("{", "").replace("}", "").replace("'","").strip(','), None,trace['Trace Message']['resp']['exception']])

    def main_process(self):
       #Get the list of tracing files
        tracing_files = os.listdir(self.trace_path)

        #Convert all files to json format and write it to the file
        for file in tracing_files:
            parsing_file = self.trace_path + "\\" + file
            traces = self.convert_to_json(parsing_file)      
            self.write_to_json_file(traces, self.json_path + "\\" + file) 
            self.backend_instance_id_magstr = []
            self.backend_instance_id_cavro = []
            self.backend_instance_id_c9 = []
            self.backend_instance_id_arduino = []
            self.backend_instance_id_ur = []
        
        #Get the list of json files
        json_files = os.listdir(self.json_path)

        #Convert all files to csv file and write it to the file
        for file in json_files:
            print(file)
            json_log_file = self.json_path + "\\" + file
            self.dumping_in_csv(json_log_file, file)
            self.backend_instance_id_magstr = []
            self.backend_instance_id_cavro = []
            self.backend_instance_id_c9 = []
            self.backend_instance_id_arduino = []
            self.backend_instance_id_ur = []
            
        #Dump it in db
        #for file in json_files:
        #    json_log_file = self.json_path + "\\" + file
        #    self.dumping_in_db(json_log_file)

if __name__ == "__main__":
    curation = Curator()
    curation.main_process()









    
