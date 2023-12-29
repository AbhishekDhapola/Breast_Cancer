from sklearn.datasets import load_breast_cancer
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Load breast cancer dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Convert DataFrame to a list of dictionaries
data_list = df.to_dict(orient='records')

# Connect to MongoDB
client = MongoClient("mongodb://your_username:your_password@your_host:your_port/your_database")
db = client.your_database  # Replace 'your_database' with the name of your MongoDB database
collection_name = 'breast_cancer_data'

# Create a new collection or use an existing one
collection = db[collection_name]

# Insert data into MongoDB
collection.insert_many(data_list)

# Close the MongoDB connection
client.close()

print(f"Breast cancer data has been imported to MongoDB in collection '{collection_name}' at {datetime.now()}")
