import kfp
from kfp import dsl
from kfp import kubernetes
from kfp import compiler

@dsl.component(
    base_image="kamalxs/mlops-cicd-architecture-image:v2"
)
def download_data():
    from regression.pipeline.Stage_01_data_preprocess import DataDownloadPreprocessPipeline
    downloader = DataDownloadPreprocessPipeline()
    downloader.main()

@dsl.component(
    base_image="kamalxs/mlops-cicd-architecture-image:v2"
)
def train_model():
    from regression.pipeline.Stage_02_model_training_pipeline import ModelTrainingPipeline
    trainer = ModelTrainingPipeline()
    trainer.main()

@dsl.component(
    base_image="kamalxs/mlops-cicd-architecture-image:v2"
)
def evaluate_model(mlflow_tracking_uri: str, mlflow_tracking_username: str, mlflow_tracking_password: str):
    import os
    import dagshub
    from regression.pipeline.Stage_03_model_evaluation_pipeline import ModelEvaluationPipeline

    # Set environment variables within the container
    os.environ['MLFLOW_TRACKING_URI'] = mlflow_tracking_uri
    os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_tracking_username
    os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_tracking_password

    # Initialize DagsHub MLflow
    # dagshub.init(repo_owner='Kamal254', repo_name='mlops-structure', mlflow=True)


    # Run the evaluation
    evaluator = ModelEvaluationPipeline()
    evaluator.main()

@dsl.pipeline(
    name="Regression Pipeline",
    description="Kubeflow Pipeline for regression task"
)
def ml_pipeline():

    pvc1 = kubernetes.CreatePVC(
        pvc_name='my-pvc',
        access_modes=['ReadWriteMany'],
        size='2Gi',
        storage_class_name='standard'
    )

    # Download Data Task
    download_task = download_data().set_caching_options(False)
    kubernetes.mount_pvc(
        download_task,
        pvc_name=pvc1.outputs['name'],
        mount_path='/app/artifacts',
    )

    # Train Model Task
    training_task = train_model().set_caching_options(False)
    kubernetes.mount_pvc(
        training_task,
        pvc_name=pvc1.outputs['name'],
        mount_path='/app/artifacts',
    )

    # Evaluate Model Task
    evaluate_task = evaluate_model(
        mlflow_tracking_uri='https://dagshub.com/Kamal254/mlops-structure.mlflow',
        mlflow_tracking_username='Kamal254',
        mlflow_tracking_password='8472dab1925bbdf273a5f943d9c9989669b3062a'
    ).set_caching_options(False)
    
    

    # Mount PVC for evaluate_task
    kubernetes.mount_pvc(
        evaluate_task,
        pvc_name=pvc1.outputs['name'],
        mount_path='/app/artifacts',
    )

    # Set task order
    training_task.after(download_task)
    evaluate_task.after(training_task)

# Compile and run the pipeline
if __name__ == '__main__':
    compiler.Compiler().compile(ml_pipeline, 'kfp_automate_pipeline.yaml')

    # Initialize KFP client
    client = kfp.Client(host='http://localhost:7080')

    pipeline_name = "Regression Automate Pipeline"
    experiment_name = "Regression Automate Experiment"
    run_name = "Regression Automate Experiment Run"

    # Upload the pipeline and get the pipeline ID and version ID
    pipeline = client.upload_pipeline('kfp_automate_pipeline.yaml', pipeline_name)
    pipeline_id = pipeline.pipeline_id

    # Create a pipeline version
    pipeline_version = client.upload_pipeline_version(
        pipeline_package_path='kfp_automate_pipeline.yaml',
        pipeline_version_name='v1',
        pipeline_id=pipeline_id
    )

    version_id = pipeline_version.pipeline_version_id
    experiment = client.create_experiment(experiment_name)

    # Run the pipeline using the pipeline ID and version ID
    run_result = client.run_pipeline(
        experiment_id=experiment.experiment_id,
        job_name=run_name,
        pipeline_id=pipeline_id,
        version_id=version_id
    )

    print(f'Pipeline {run_result.run_id} is running')
