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


            allDataDictionary=get_all_data
            print(allDataDictionary)
            print(type(allDataDictionary))
           # str1 = str(allDataDictionary)


            for value in allDataDictionary:
                if(type(allDataDictionary[value]) ==  numpy.ndarray):
                    allDataDictionary[value]=str(allDataDictionary[value])

            DataInjson = json.dumps(allDataDictionary,indent = 4)

            #working code for mongo DB
            client=MongoClient("localhost",27017)
            db=client["dataFromSim"]
            collectionTraces=db["commandTraces"]
            collectionTraces.insert_one(allDataDictionary)

            with open('bookForData.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in allDataDictionary.items():
                    writer.writerow([key, value])

            print("##########\t##########\t##########\t##########")

            time.sleep(1)
            break

        #except:
            pass

    r.close()
