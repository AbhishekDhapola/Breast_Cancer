import os
import sys
from configparser import ConfigParser
import pandas as pd
from pymongo import MongoClient
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join("artifact_folder")
    config_file_path: str = os.path.join("config", "config.ini")


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.data_ingestion_config = config
        self.config_parser = ConfigParser()
        self.config_parser.read(self.data_ingestion_config.config_file_path)

        # Retrieve MongoDB configuration from the config file
        self.db_user = self.config_parser.get("MongoDB", "DB_USER")
        self.db_password = self.config_parser.get("MongoDB", "DB_PASSWORD")
        self.db_name = self.config_parser.get("MongoDB", "DB_NAME")
        self.collection_name = self.config_parser.get("MongoDB", "COLLECTION_NAME")

    def export_collection_as_dataframe(self, collection_name="default_collection", db_name="default_db"):
        try:
            mongo_db_url = f"mongodb+srv://{self.db_user}:{self.db_password}@cluster0.bodyzyl.mongodb.net/?retryWrites=true&w=majority"
            logging.info(f"MongoDB connection URL: {mongo_db_url}")
            mongo_client = MongoClient(mongo_db_url)
            
            db_name = db_name if db_name != "default_db" else self.db_name
            collection_name = collection_name if collection_name != "default_collection" else self.collection_name
            
            db = mongo_client[db_name]
            collection = db[collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": pd.NA}, inplace=True)
            return df

        except Exception as e:
            raise CustomException(e, sys)

    def export_data_into_feature_store_file_path(self):
        try:
            logging.info("Exporting data from MongoDB")
            os.makedirs(self.data_ingestion_config.artifact_folder, exist_ok=True)

            sensor_data = self.export_collection_as_dataframe()

            logging.info(f"Saving exported data into feature store file path: {self.data_ingestion_config.artifact_folder}")

            feature_store_file_path = os.path.join(self.data_ingestion_config.artifact_folder, "breast_cancer.csv")
            sensor_data.to_csv(feature_store_file_path, index=False)

            return feature_store_file_path

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> str:
        try:
            logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

            feature_store_file_path = self.export_data_into_feature_store_file_path()

            logging.info("Got the data from MongoDB")

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")

            return feature_store_file_path

        except Exception as e:
            raise CustomException(e, sys) from e

