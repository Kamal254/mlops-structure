from regression.components.model_training_component import ModelTraining
from regression.config.configuration import ConfigurationManager
from regression import logger

STAGE_NAME = "Training Model"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        model_config = config_manager.get_model_config()
        model_training = ModelTraining(model_config)
        model_training.split_data()
        model_training.train_model()

if __name__ == '__main__':
    try:
        logger.info(f'>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<')
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f'>>>>>>>>>> Stage {STAGE_NAME} Completed <<<<<<<<<<')
    except Exception as e:
        logger.exception(f'Getting Exception {e}')
        raise e

