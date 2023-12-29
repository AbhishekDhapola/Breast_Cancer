# import_data.py
from pymongo import MongoClient
import pandas as pd
import json
import configparser

# Read configuration from the config file
config = configparser.ConfigParser()
config.read("./config/config.ini")

# Retrieve values from the configuration
db_user = config.get("MongoDB", "DB_USER")
db_password = config.get("MongoDB", "DB_PASSWORD")
db_name = config.get("MongoDB", "DB_NAME")
collection_name = config.get("MongoDB", "COLLECTION_NAME")

# MongoDB Atlas connection URI
uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.bodyzyl.mongodb.net/?retryWrites=true&w=majority"

# CSV file path
csv_file_path = "./notebook/breast_cancer_data.csv"
df = pd.read_csv(csv_file_path)

# Convert DataFrame to JSON records
json_records = json.loads(df.T.to_json()).values()

# Connect to MongoDB Atlas cluster
client = MongoClient(uri)

# Access the specified database and collection
db = client[db_name]
collection = db[collection_name]

# Insert JSON records into the collection
try:
    collection.insert_many(json_records)
    print("Data successfully inserted into MongoDB Atlas.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the MongoDB connection
    client.close()
