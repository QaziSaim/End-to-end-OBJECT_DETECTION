from src.vehicle.components.data_validation import DataValidation
from src.vehicle.logging.logger import logger
from src.vehicle.exception.exception import CustomException
from src.vehicle.components.model_trainer import ModelTrainer
import sys
class TrainPipeline:
    def __init__(self):
        self.data_path = 'data/BoneFractureYolo8'
        self.data_yaml_path = 'data/BoneFractureYolo8/data.yaml'
    def run_pipeline(self):
        try:
            logger.info('Starting Data Validation')
            
            validator = DataValidation(data_path=self.data_path)
            validator.run_validation()

            logger.info("Data Validation Completed")

            trainer = ModelTrainer(data_yaml_path=self.data_yaml_path)
            trainer.train()

            logger.info('Model Training Completed')
        except Exception as e:
            raise CustomException(e,sys)