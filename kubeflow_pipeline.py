import kfp
from kfp import dsl
from kfp import kubernetes
from kfp import compiler

from regression import logger
from regression.pipeline.Stage_01_data_preprocess import DataDownloadPreprocessPipeline
from regression.pipeline.Stage_02_model_training_pipeline import ModelTrainingPipeline
from regression.pipeline.Stage_03_model_evaluation_pipeline import ModelEvaluationPipeline

@dsl.component(
        base_image = "kamalxs/mlops-architecture-image:v3"
)
def download_data():
    from regression.pipeline.Stage_01_data_preprocess import DataDownloadPreprocessPipeline
    downloader = DataDownloadPreprocessPipeline()
    downloader.main()



@dsl.component(
    base_image = "kamalxs/mlops-architecture-image:v3"
)
def train_model():
    from regression.pipeline.Stage_02_model_training_pipeline import ModelTrainingPipeline
    trainer = ModelTrainingPipeline()
    trainer.main()
    


@dsl.component(
        base_image = "kamalxs/mlops-architecture-image:v3"
)
def evaluate_model():
    from regression.pipeline.Stage_03_model_evaluation_pipeline import ModelEvaluationPipeline
    evaluator = ModelEvaluationPipeline()
    evaluator.main()


@dsl.pipeline(
    name = "Regression Pipeline",
    description="kubeflow Pipeline for regression task"
)

def ml_pipeline():

    pvc1 = kubernetes.CreatePVC(
        pvc_name = 'my-pvc',
        access_modes = ['ReadWriteMany'],
        size = '2Gi',
        storage_class_name = 'standard'

    )

    download_task = download_data().set_caching_options(False)
    kubernetes.mount_pvc(
        download_task,
        pvc_name=pvc1.outputs['name'],
        mount_path='app/artifacts',
    )

    training_task = train_model().set_caching_options(False)
    kubernetes.mount_pvc(
        training_task,
        pvc_name=pvc1.outputs['name'],
        mount_path='app/artifacts',
    )

    evaluate_task = evaluate_model().set_caching_options(False)
    kubernetes.mount_pvc(
        evaluate_task,
        pvc_name=pvc1.outputs['name'],
        mount_path='app/artifacts',
    )


    training_task.after(download_task)
    evaluate_task.after(training_task)

if __name__ == '__main__':
    compiler.Compiler().compile(ml_pipeline, 'kfp_test1_pipeline.yaml')


