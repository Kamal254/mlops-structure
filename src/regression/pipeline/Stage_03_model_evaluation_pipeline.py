from regression.components.model_evaluation_component import Evaluation
from regression.config.configuration import ConfigurationManager
from regression import logger

STAGE_NAME = "Model Evaluation"

class ModelEvaluationPipeline():
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        eval_config = config_manager.get_evaluation_config()
        model_eval = Evaluation(eval_config)
        model_eval.load_model()
        model_eval.evaluation()
        model_eval.log_into_mlflow()

if __name__ == '__main__':
    try:
        logger.info(f'>>>>>>>>>> Stage {STAGE_NAME} Started <<<<<<<<<<')
        obj = ModelEvaluationPipeline()
        obj.main()
        logger.info(f'>>>>>>>>>> Stage {STAGE_NAME} Completed <<<<<<<<<<')
    except Exception as e:
        logger.exception(f'Getting Exception {e}')
        raise e

        
