import time
import logging
import sys
import os
import json
import csv
import numpy
from pymongo import MongoClient


#sys.path.append(r"C:\Users\LBRY-SVC-Patron\Desktop\moduals\python-urx-master")# change the path to where the folder for urx is when start to run the code 
#importing urx may require some special steps, unlike other imports
import urx

import getopt
import sys

import argparse
from datetime import datetime



parser = argparse.ArgumentParser(description='get following information: IP address, frequency, database client name, and output csv file name. (e.g. "0.0.0.0 2 DBname fileName.csv")')
                 
parser.add_argument('ip_address', metavar='string(IP)', type=str, 
                    help='a str to get ip address')

parser.add_argument('frequency', metavar='integer(frequency)', type=int, 
                    help='an int for  frequency')

parser.add_argument('data_base_client', metavar='string(DB name)', type=str, 
                    help='a str for data base client name')

parser.add_argument('output_filename', metavar='string(out file name)', type=str,
                    help='a str for output file name')

args = parser.parse_args()

print("\nip address:")
print(args.ip_address)
print("\nfrequency:")
print(args.frequency)
print("\nDB client name:")
print(args.data_base_client)
print("\nCSV file name:")
print(args.output_filename)
print("\n")


ip_address=args.ip_address
frequency=args.frequency
data_base_client=args.data_base_client
output_filename=args.output_filename

isFirstTimeToRun=1


#old code to get arg from command line

# getting arg from command line
#ip_address = "0.0.0.0"
#frequency = 1
#data_base_client="data_from_sim"
#output_filename = "bookForData.csv"

#options, remainder = getopt.gnu_getopt(sys.argv[1:], 'o:v',['ip_address=', 'frequency=','data_base_client=','output_filename=',])

#for opt, arg in options:
#    if opt == '--ip_address':
#        ip_address = arg
#    elif opt == '--frequency':
#        frequency = arg
#    elif opt == '--data_base_client':
#        data_base_client = arg
#    elif opt == '--output_filename':
#        output_filename = arg
# end of gettting arg from command line




r = urx.Robot(ip_address, use_rt=True, urFirm=5.1)

if __name__ == "__main__":
    while 1:
        try:
            get_all_data = r.get_all_rt_data()

            all_data_dictionary=get_all_data
            all_data_dictionary['_id']=all_data_dictionary['timestamp']
            del all_data_dictionary['timestamp']

            print(get_all_data)

            for value in all_data_dictionary:
                if(type(all_data_dictionary[value]) ==  numpy.ndarray):
                    all_data_dictionary[value]=str(all_data_dictionary[value])

            #data_in_json = json.dumps(all_data_dictionary,indent = 4)

            #working code for mongo DB
            client=MongoClient("localhost",27017)
            db=client[data_base_client]
            collection_traces=db["command_traces"]
            collection_traces.insert_one(all_data_dictionary)

            

            
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M")
            isOutPutFileEsist=os.path.isfile(output_filename)
            dt_string=dt_string.replace(" ","--")
            dt_string=dt_string.replace(":","-")
            dt_string=dt_string.replace("/","-")
            
            #the following 4 lines of code are to add data and time to file name, and they can be commented out if not needed
            if(isFirstTimeToRun==1):
                output_filename+=dt_string
            
                output_filename=output_filename.replace(".csv","")
                output_filename=output_filename.replace(".CSV","")
                output_filename+='.csv'
                isFirstTimeToRun=0

            isOutPutFileEsist=os.path.isfile(output_filename)

            
            
            with open(output_filename, 'a' ,newline='') as csv_file:
                writer = csv.writer(csv_file)
                header = []
                data = []
                
                header.append('_id')
                data.append(all_data_dictionary['_id'])

                for key, value in all_data_dictionary.items():
                    header.append(key)
                    data.append(value)
                if(isOutPutFileEsist == False):
                    writer.writerow(header)
                writer.writerow(data)

            print("end of excution ##########\t##########\t##########\t##########")

            time.sleep(frequency)
            break
        except:
            pass
        
    r.close()
