from regression.constants import constant
from regression.utils.common_func import read_yaml, create_dir
from regression.entity.config_entity import DatabaseCredentials, DataIngestionConfig, ModelTrainingConfig, ModelEvaluationConfig

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = constant.CONFIG_FILE_PATH,
        param_filepath = constant.PARAMS_FILE_PATH,
        secret_filepath = constant.SECRET_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(param_filepath)
        self.secret = read_yaml(secret_filepath)

        create_dir([self.config.root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_paths

        create_dir([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            download_folder_path=config.download_folder_path,
            local_data_file=config.local_data_file,
            processed_data=config.processed_data

        )

        return data_ingestion_config
    
    def get_database_credentials(self) -> DatabaseCredentials:
        cred_config = self.secret.database_cred

        credentials_data = DatabaseCredentials(
            db_user= cred_config.db_user,
            db_password=cred_config.db_password,
            db_host=cred_config.db_host,
            db_port=cred_config.db_port,
            db_name=cred_config.db_name
        )

        return credentials_data
    
    def get_model_config(self) -> ModelTrainingConfig:
        prepare_model_config = self.config.prepare_model
        data_config = self.config.data_paths
        data_split_config = self.config.data_split
        create_dir([prepare_model_config.root_dir])

        model_config = ModelTrainingConfig(
            root_dir = prepare_model_config.root_dir,
            model_file_path = prepare_model_config.model_file_path,
            data_path = data_config.processed_data,
            criterion = self.params.criterion,
            max_depth = self.params.max_depth,
            test_data_filepath = data_split_config.test_data_filepath,
            train_data_filepath = data_split_config.train_data_filepath
        )

        return model_config
    

    def get_evaluation_config(self) -> ModelEvaluationConfig:
        eval_config = ModelEvaluationConfig(
            model_file_path = self.config.prepare_model.model_file_path,
            test_data_filepath=self.config.data_split.test_data_filepath,
            criterion=self.params.criterion,
            max_depth=self.params.max_depth)
        return eval_config
    