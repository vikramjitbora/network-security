import os
import json
import sys
from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("MongoDB connection URL is not set in the environment variables.")

CA_CERT_PATH = certifi.where()

class NetworkDataExtract:
    def __init__(self, mongo_url: str = MONGO_DB_URL):
        try:
            self.mongo_client = pymongo.MongoClient(mongo_url)
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {str(e)}")
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def csv_to_json_converter(file_path: str):
        """Converts CSV data to JSON format."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            data = pd.read_csv(file_path)
            if data.empty:
                logging.warning("CSV file is empty.")
                return []
            
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.to_json(orient='records'))
            return records
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {str(e)}")
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records: list, database_name: str, collection_name: str):
        """Inserts JSON data into MongoDB."""
        try:
            if not records:
                logging.warning("No records to insert into MongoDB.")
                return 0
            
            database = self.mongo_client[database_name]
            collection = database[collection_name]
            result = collection.insert_many(records)
            logging.info(f"Inserted {len(result.inserted_ids)} records into MongoDB.")
            return len(result.inserted_ids)
        except Exception as e:
            logging.error(f"Error inserting data into MongoDB: {str(e)}")
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "NETWORKSEC"
    COLLECTION = "NetworkData"
    
    try:
        network_obj = NetworkDataExtract()
        records = network_obj.csv_to_json_converter(FILE_PATH)
        num_records = network_obj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
        print(f"Successfully inserted {num_records} records.")
    except Exception as e:
        logging.error(f"Error in execution: {str(e)}")
        raise NetworkSecurityException(e, sys)
