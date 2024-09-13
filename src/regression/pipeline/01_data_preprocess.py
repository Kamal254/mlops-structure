from regression.config.configuration import ConfigurationManager
from regression.components.data_component import DataIngestion



try:
    config_manager = ConfigurationManager()
    data_ingestion_config = config_manager.get_data_ingestion_config()
    db_credentials_config = config_manager.get_database_credentials()
    data_ingestion_preprocess = DataIngestion(data_ingestion_config, db_credentials_config)
    data_ingestion_preprocess.download_data()
    data_ingestion_preprocess.transform_data()
except Exception as e:
    raise e