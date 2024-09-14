
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

from regression.entity.config_entity import ModelTrainingConfig
from regression.constants import constant
from regression.utils.common_func import read_yaml, create_dir
from regression import logger
import joblib


class ModelTraining:
    def __init__(self, config:ModelTrainingConfig):
        self.config = config
        
    def split_data(self) -> str:
        try:
            logger.info(f'Loading Dataset from {self.config.data_path} into Datafram')
            df = pd.read_csv(self.config.data_path)
            logger.info("Splitting the dataset into train and test datasets")
            train_dataset = df[:1450]
            test_dataset = df[1450:]
            logger.info("Saving train and test data into artifact folder")
            train_dataset.to_csv(self.config.train_data_filepath)
            test_dataset.to_csv(self.config.test_data_filepath)
        except Exception as e:
            raise e
    

    def train_model(self) ->str:
        try:
            logger.info("Loading Training Data into dataframe")
            df = pd.read_csv(self.config.test_data_filepath)
            y = df['quality']
            x = df.drop('quality', axis=1)
            logger.info("splitting the data into X and y")
            logger.info("defining the model")

            classifier = DecisionTreeClassifier(criterion = self.config.criterion, max_depth=self.config.max_depth)
            logger.info("Training Model .........")
            classifier.fit(x, y)

            logger.info("Model is successfully trained")

            joblib.dump(classifier, self.config.model_file_path)

            logger.info("Model is successfully saved at {self.config.model_file_path}")
        
        except Exception as e:
            logger.error(f"Error Occurred during model training {e}")
            raise e