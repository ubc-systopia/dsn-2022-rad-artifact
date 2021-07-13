import time
import logging
import sys
import os
from pymongo import MongoClient

# file_path = os.path.dirname(os.path.abspath(__file__))
# urx_path = os.path.dirname(os.path.dirname(file_path))
# python_urx_path = os.path.join(urx_path, "python-urx-master")
# sys.path.append(python_urx_path)


sys.path.append(r"C:\Users\LBRY-SVC-Patron\Desktop\moduals\python-urx-master")
import urx


import json
import csv
import numpy

r = urx.Robot("192.168.229.128", use_rt=True, urFirm=5.1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    while 1:
        #try:
            get_all_data = r.get_all_rt_data()
            print(get_all_data)

            all_data_dictionary=get_all_data

            for value in all_data_dictionary:
                if(type(all_data_dictionary[value]) ==  numpy.ndarray):
                    all_data_dictionary[value]=str(all_data_dictionary[value])

            data_in_json = json.dumps(all_data_dictionary,indent = 4)

            #working code for mongo DB
            client=MongoClient("localhost",27017)
            db=client["dataFromSim"]
            collection_traces=db["commandTraces"]
            collection_traces.insert_one(all_data_dictionary)

            with open('bookForData.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in all_data_dictionary.items():
                    writer.writerow([key, value])

            print("##########\t##########\t##########\t##########")

            time.sleep(1)
            break

        #except:
            pass

    r.close()
