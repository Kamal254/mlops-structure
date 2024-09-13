import os
from regression import logger
import gdown
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from regression.entity.config_entity import DatabaseCredentials, DataIngestionConfig

class DataIngestion:
    def __init__(self, config:DataIngestionConfig, db_config: DatabaseCredentials):
        self.config = config
        self.db_config = db_config

    def download_data(self) -> str:
        try:
            dataset_url = self.config.source_URL
            download_file = self.config.local_data_file
            os.makedirs(self.config.root_dir, exist_ok = True)
            logger.info(f"Downloading Data from {dataset_url} into {download_file}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix+file_id, download_file)

            logger.info(f'Downloaded data from {dataset_url} into file {download_file}')

        except Exception as e:
            raise e
        
    def preprocess_data(self, rawdata_filepath) ->str:
        #preprocessing of data will complete by this function
        #Save the preprocessed data into local database
        processed_data_filepath = self.config.processed_data
        dataframe = pd.read_csv(rawdata_filepath)
        logger.info("Dataset Loaded in Dataframe")
        """
                Do the Preprocessing Steps Here       
        
        """

        logger.info(f"Preprocessing Completed")
        dataframe.to_csv(processed_data_filepath, index=False)
        logger.info(f'Processed Data Saved into file {processed_data_filepath}') 

        connection_string = f'postgresql+psycopg2://{self.db_config.db_user}:{self.db_config.db_password}@{self.db_config.db_host}:{self.db_config.db_port}/{self.db_config.db_name}'
        
        logger.info(f'connecting to database at {connection_string}')

        try:
            engine = create_engine(connection_string)
        except Exception as e:
            raise e
        
        logger.info("connection made to local pgadmin server")

        preprocessed_data = pd.read_csv(processed_data_filepath)
        table_name = 'whine_quality'
        preprocessed_data.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info("Successfully created table into Local Database")

    def transform_data(self) -> str:
        rawdata_filepath = self.config.local_data_file
        dataframe = pd.read_csv(rawdata_filepath)
        if(not dataframe.empty):
            logger.info(f'preprocessing data ...')
            self.preprocess_data(rawdata_filepath)
        else:
            logger.info(f'No file present in the {rawdata_filepath}')