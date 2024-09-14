# Init Logging functionality

import os
import sys
import logging

logging_str = "[%(asctime)s:%(levelname)s:%(module)s:%(message)s]"

logging_directory = "../../../logs"
log_filepath = os.path.join(logging_directory, "running_logs.log")
os.makedirs(logging_directory, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("regressionLogger")