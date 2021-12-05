# Extract RAD_Commands

## Extracing csv.zip

* Unzip `csv.zip` using any file archiver and compressor. 

## Extracting mongodb.zip

* Unzip `mongodb.zip` using any file archiver and compressor that contains `commandTraces.json` file.
* Install [MongoDB Database tool](https://www.mongodb.com/try/download/database-tools).
* Import the json file into MongoDB using the command-line:
  `mongoimport --db <database name> --collection <collection name> --file commandTraces.json`
* Install [MongoDB Compass](https://www.mongodb.com/try/download/compass) that is GUI for MongoDB. 
