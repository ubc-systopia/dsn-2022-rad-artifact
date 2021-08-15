import time
import logging
import sys
import os
import json
import csv
import numpy
from pymongo import MongoClient
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

OUTOUT_FILENAME_CONST=output_filename
last_time=""

isFirstTimeToRun=1

r = urx.Robot(ip_address, use_rt=True, urFirm=5.1)

if __name__ == "__main__":
    while 1:
        try:
            get_all_data = r.get_all_rt_data()

            all_data_dictionary=get_all_data
            all_data_dictionary['_id']=all_data_dictionary['timestamp']
            del all_data_dictionary['timestamp']

            print(get_all_data)


            new_data_to_add_to_all_data_dictionary={}
            for key in all_data_dictionary:
                if(type(all_data_dictionary[key]) ==  numpy.ndarray):
                    if(all_data_dictionary[key].ndim != 0):
                        indexCounter=0

                        for x in all_data_dictionary[key]:
                            newKeyToAdd=key+"-index-"+str(indexCounter)
                            new_data_to_add_to_all_data_dictionary[newKeyToAdd]=x
                            indexCounter+=1
            all_data_dictionary.update(new_data_to_add_to_all_data_dictionary)



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
            
            
            
            now = datetime.now()
            date_string = now.strftime("%d/%m/%Y")
            if(last_time != date_string): # a new day or run for first time, so create a new file
                isFirstTimeToRun=1
                output_filename=OUTOUT_FILENAME_CONST
                last_time=date_string
            
            
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
                del all_data_dictionary['_id']

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
