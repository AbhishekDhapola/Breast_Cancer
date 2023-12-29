import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import DataIngestionConfig
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException

class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            # Assuming you have already defined your DataIngestionConfig class and its methods
            config = DataIngestionConfig()

            # Create an instance of DataIngestion with the configuration
            
            data_ingestion = DataIngestion(config)
            feature_store_file_path = data_ingestion.initiate_data_ingestion()
            return feature_store_file_path

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, feature_store_file_path):
        try:
            data_transformation = DataTransformation(feature_store_file_path=feature_store_file_path)
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation()
            
            return train_arr, test_arr, preprocessor_path

        except Exception as e:
            raise CustomException(e, sys)

    def start_model_training(self, train_arr, test_arr):
        try:
            model_trainer = ModelTrainer()
            
            
            
            model_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
            return model_score

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            feature_store_file_path = self.start_data_ingestion()
            train_arr, test_arr, preprocessor_path = self.start_data_transformation(feature_store_file_path)
            
            r2_square = self.start_model_training(train_arr, test_arr)

            print("Training completed. Trained model score: ", r2_square)

        except Exception as e:
            raise CustomException(e, sys)

