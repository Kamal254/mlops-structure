from regression.config.configuration import ConfigurationManager
from regression.components.data_component import DataIngestion
from regression import logger


STAGE_NAME = "Download & Preprocess Data"

class DataDownloadPreprocessPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        data_ingestion_config = config_manager.get_data_ingestion_config()
        db_credentials_config = config_manager.get_database_credentials()
        data_ingestion_preprocess = DataIngestion(data_ingestion_config, db_credentials_config)
        data_ingestion_preprocess.download_data()
        data_ingestion_preprocess.transform_data()



if __name__ == '__main__':
    try:
        logger.info(f'>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<')
        obj = DataDownloadPreprocessPipeline()
        obj.main()
        logger.info(f'>>>>>>>>>> Stage {STAGE_NAME} Completed <<<<<<<<<<')
    except Exception as e:
        logger.exception(f'Getting Exception {e}')
        raise e