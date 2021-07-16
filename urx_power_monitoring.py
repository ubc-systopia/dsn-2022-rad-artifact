import time
import logging
import sys
import os
import json
import csv
import numpy
from pymongo import MongoClient

# file_path = os.path.dirname(os.path.abspath(__file__))
# urx_path = os.path.dirname(os.path.dirname(file_path))
# python_urx_path = os.path.join(urx_path, "python-urx-master")
# sys.path.append(python_urx_path)

#sys.path.append(r"C:\Users\LBRY-SVC-Patron\Desktop\moduals\python-urx-master")# change the path to where the folder for urx is when start to run the code 

#importing urx may require some special steps, unlike other imports
import urx

import getopt
import sys




# getting arg from command line
ip_address = "0.0.0.0"
frequency = 1
data_base_client="data_from_sim"
output_filename = "bookForData.csv"

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:v',['ip_address=', 'frequency=','data_base_client=','output_filename=',])

for opt, arg in options:
    if opt == '--ip_address':
        ip_address = arg
    elif opt == '--frequency':
        frequency = arg
    elif opt == '--data_base_client':
        data_base_client = arg
    elif opt == '--output_filename':
        output_filename = arg
 # end of gettting arg from command line




r = urx.Robot(ip_address, use_rt=True, urFirm=5.1) # change the ip address when start to run the code

if __name__ == "__main__":
    while 1:
        try:
            get_all_data = r.get_all_rt_data()
            print(get_all_data)

            all_data_dictionary=get_all_data

            for value in all_data_dictionary:
                if(type(all_data_dictionary[value]) ==  numpy.ndarray):
                    all_data_dictionary[value]=str(all_data_dictionary[value])

            data_in_json = json.dumps(all_data_dictionary,indent = 4)

            #working code for mongo DB
            client=MongoClient("localhost",27017)
            db=client[data_base_client]
            collection_traces=db["command_traces"]
            collection_traces.insert_one(all_data_dictionary)

            with open('output_filename', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in all_data_dictionary.items():
                    writer.writerow([key, value])

            print("end of excution ##########\t##########\t##########\t##########")

            time.sleep(frequency)
            break

        except:
            pass

    r.close()
