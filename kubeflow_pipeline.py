import kfp
from kfp import dsl
# from kfp.components import create_component_from_func
from kfp import compiler

from regression import logger
from regression.pipeline.Stage_01_data_preprocess import DataDownloadPreprocessPipeline
from regression.pipeline.Stage_02_model_training_pipeline import ModelTrainingPipeline
from regression.pipeline.Stage_03_model_evaluation_pipeline import ModelEvaluationPipeline

@dsl.component
def download_data():
    downloader = DataDownloadPreprocessPipeline()
    return downloader.main()


@dsl.component
def train_model():
    trainer = ModelTrainingPipeline()
    return trainer.main()


@dsl.component
def evaluate_model():
    evaluator = ModelEvaluationPipeline()
    return evaluator.main()

download_data_op = download_data
train_model_op = train_model
evaluate_model_op = evaluate_model


@dsl.pipeline(
    name = "Regression Pipeline",
    description="kubeflow Pipeline for regression task"
)

def ml_pipeline():
    download_task = download_data_op()
    training_task = train_model_op()
    evaluate_task = evaluate_model_op()

if __name__ == '__main__':
    compiler.Compiler().compile(ml_pipeline, 'ml_pipeline.yaml')
