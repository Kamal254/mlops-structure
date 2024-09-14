# This file contain the custom return type entities.

from pathlib import Path
from dataclasses import dataclass

"""
    DataIngestion Configuration Variable types
"""
@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    source_URL : str
    download_folder_path : Path
    local_data_file : Path
    processed_data : Path


"""
    PGadmin Database Credentials Configuration
"""
@dataclass(frozen=True)
class DatabaseCredentials:
    db_user : str
    db_password : str
    db_host : str
    db_port : int
    db_name : str


"""
    Model Training Configuration
"""
@dataclass(frozen=True)
class ModelTrainingConfig:
    root_dir : Path
    model_file_path : Path
    data_path : Path
    criterion : str
    max_depth : int
    test_data_filepath : Path
    train_data_filepath : Path



"""
    Model Evaluation Configuration
"""
@dataclass(frozen=True)
class ModelEvaluationConfig:
    model_file_path : Path
    test_data_filepath : Path
    criterion : str
    max_depth : int