
from regression.constants import constant
from regression.utils.common_func import read_yaml, create_dir, save_json
from regression import logger
from regression.entity.config_entity import ModelEvaluationConfig
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, r2_score

import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
from mlflow.models import infer_signature




class Evaluation:
    def __init__(self, config : ModelEvaluationConfig):
        self.config = config

    def load_model(self) ->str:
        try:
            logger.info(f'loading the model from {self.config.model_file_path}')
            self.model = joblib.load(self.config.model_file_path)
            logger.info("Model loaded Successfully")

        except Exception as e:
            logger.error(f"Error occurred while loading the model: {e}")
            raise e
        
    def evaluation(self) ->str:
        logger.info(f'loading test data into dataframe')
        test_df = pd.read_csv(self.config.test_data_filepath)
        y_test = test_df['quality']
        x_test = test_df.drop('quality', axis=1)
        logger.info("Predicting Model Output and Calculating Score")
        y_pred = self.model.predict(x_test)
        self.score = accuracy_score(y_test, y_pred)
        self.rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        self.mae = mean_absolute_error(y_test, y_pred)
        self.r2 = r2_score(y_test, y_pred)

    def log_into_mlflow(self):
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        logger.info("Saving Experiments to the mlflow")
        with mlflow.start_run():
            test_df = pd.read_csv(self.config.test_data_filepath)
            y_test = test_df['quality']
            x_test = test_df.drop('quality', axis=1)
            # y_pred = self.model.predict(x_test)
            mlflow.log_param("criterion", self.config.criterion)
            mlflow.log_param("max_depth", self.config.max_depth)

            mlflow.log_metric("RMSE", self.rmse)
            mlflow.log_metric("MAE", self.mae)
            mlflow.log_metric("R2", self.r2)

            signature = infer_signature(y_test, self.model.predict(x_test))

            if tracking_url_type_store != "file":

                # Register the model
                # There are other ways to use the Model Registry, which depends on the use case,
                # please refer to the doc for more information:
                # https://mlflow.org/docs/latest/model-registry.html#api-workflow
                mlflow.sklearn.log_model(self.model, "model", registered_model_name="DescisionClassifier")
            else:
                mlflow.sklearn.log_model(self.model, "model", signature=signature)