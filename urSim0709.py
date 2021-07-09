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
                print(type(allDataDictionary[value]))
                print(allDataDictionary[value])

                #if(isinstance(value, list)):
                if(type(allDataDictionary[value]) ==  'numpy.ndarray'):
                    print("met a list1")
                    print(type(allDataDictionary[value]))
                    allDataDictionary[value]=str(allDataDictionary[value])
                    print(type(allDataDictionary[value]))


                if(type(allDataDictionary[value]) ==  numpy.ndarray):
                    print("met a list2")
                    print(type(allDataDictionary[value]))
                    allDataDictionary[value]=str(allDataDictionary[value])
                    print(type(allDataDictionary[value]))

                if(type(allDataDictionary[value]) == list):
                    print("met a list3")
                    print(type(allDataDictionary[value]))
                    allDataDictionary[value]=str(allDataDictionary[value])
                    print(type(allDataDictionary[value]))




            # allDataDictionaryToList = allDataDictionary.tolist()
            # print(allDataDictionaryToList)

            #lists = allDataDictionary.tolist()

            # convert into JSON:
            DataInjson = json.dumps(allDataDictionary,indent = 4)
           # y = json.loads(str1)

            # with open('data2.csv', 'w', newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerow(["header"])
            #     writer.writerow([i, allDataDictionary])






            #working code for mongo DB
            client=MongoClient("localhost",27017)
            db=client["dataFromSim"]
            collectionTraces=db["commandTraces"]
            collectionTraces.insert_one(allDataDictionary)
            











            # j_temp = r.get_joint_temperature()
            # j_voltage = r.get_joint_voltage()
            # j_current = r.get_joint_current()
            # main_voltage = r.get_main_voltage()
            # robot_voltage = r.get_robot_voltage()
            # robot_current = r.get_robot_current()

         #   print("JOINT TEMPERATURE")
         #   print(j_temp)

         #   print("JOINT VOLTAGE")
         #   print(j_voltage)

         #   print("JOINT CURRENT")
         #   print(j_current)

        #    print("MAIN VOLTAGE")
         #   print(main_voltage)

         #   print("ROBOT VOLTAGE")
         #   print(robot_voltage)

         #   print("ROBOT CURRENT")
         #   print(robot_current)




            with open('bookForData.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in allDataDictionary.items():
                    writer.writerow([key, value])







            #read back, not needed here
            # with open('Book1.csv') as csv_file:
            #     reader = csv.reader(csv_file)
            #     mydict = dict(reader)



            print("##########\t##########\t##########\t##########")

            time.sleep(1)
            break

        #except:
            pass

    r.close()
