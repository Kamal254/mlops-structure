# This file contain the custom return type entities.

from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir : Path
    source_URL : str
    download_folder_path : Path
    local_data_file : Path
    processed_data : Path

@dataclass(frozen=True)
class DatabaseCredentials:
    db_user : str
    db_password : str
    db_host : str
    db_port : int
    db_name : str