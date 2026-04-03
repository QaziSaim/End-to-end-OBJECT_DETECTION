from src.boneFractureDetection.logging.logger import logger
from src.boneFractureDetection.exception.exception import CustomException
import sys

try:
    logger.info("End Training...")
    x = 1 / 0  # error
except Exception as e:
    raise CustomException(e, sys)