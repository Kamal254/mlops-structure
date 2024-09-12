# from src.regression.components.test import check
# check()

# from src.regression.entity.testprint import checkprint
# checkprint()

from src.regression.pipeline.testpipeline import testpipe
testpipe()

from regression import logger
logger.info("Logger is working")