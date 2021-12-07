# Extracting RAD Commands

## Extracing csv.zip

* Unzip `csv.zip` using any file archiver and compressor. 

## Extracting mongodb.zip

* Unzip `mongodb.zip` using any file archiver and compressor that contains `commandTraces.json` file.
* Install [MongoDB Database tool](https://www.mongodb.com/try/download/database-tools).
* Import the json file into MongoDB using the command-line:
  `mongoimport --db <database name> --collection <collection name> --file commandTraces.json`
* Install [MongoDB Compass](https://www.mongodb.com/try/download/compass) - GUI for MongoDB.

# MongoDB Queries

Here is a list of MongoDB queries (MongoDB Compass) that will be helpful in filering the required data:

* Get all data : `{}`

  For example `{}` retrieves all documents.
  
* Filtering data on particular fields and values : `{<field1> : <value1>, <field2> : <value2>, ...}` 

  For example `{"Trace Message.req.method_name" : "move_joints"}` retrieves documents where the method name is 'move_joints'.
  
* Filtering data on the basis of query operators: `{ <field1>: { <operator1>: <value1> }, <field2>: { <operator2>: <value2> }, ... }`

  For example `{'Trace Message.req.method_name' : {$in : ["move_joints", "open_gripper"]}}` retrieves documents where the method name is either 'move_joints' or 'open_gripper'.
  
* Filtering data using 'And' operator: 

  For example `{'Trace Message.req.method_name' : "open_gripper" , 'Trace Message.req.args.position' : {$eq: '0.5'}}` retreives documents where the method name is 'open_gripper' and the gripper position equals '0.5'.
 
* Filtering data using 'OR' operator:

  For example `{$or: [{'Trace Message.req.method_name' : "open_gripper" , 'Trace Message.req.args.position' : {$eq: '0.5'}}]}` retreives documents where the method name is 'open_gripper' or the gripper position equals '0.5'.
 
 ## Additional Documents
Guide to write MongoDB queries : https://docs.mongodb.com/manual/tutorial/query-documents/
  
