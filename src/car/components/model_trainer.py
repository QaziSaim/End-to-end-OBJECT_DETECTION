from ultralytics import YOLO
import os   
import sys
from src.boneFractureDetection.logging.logger import logger
from src.boneFractureDetection.exception.exception import CustomException

class ModelTrainer:
    def __init__(self,data_yaml_path:str):
        self.data_yaml_path = data_yaml_path
        self.model_path = 'yolov8s.pt'
        self.artifact_dir = 'artifact/model'

        os.makedirs(self.artifact_dir,exist_ok=True)
    
    def train(self):
        try:
            logger.info('Initilizing YOLOV8s model...')

            model = YOLO(self.model_path)

            logger.info('Starting model training...')

            model.train(
                data = self.data_yaml_path,
                epochs=50,
                imgsz=640,
                batch=8,
                device=0
            )

            logger.info('Training Completed')

            trained_model_path = 'runs/detect/train/weights/best.pt'

            if os.path.exists(trained_model_path):
                final_path = os.path.join(self.artifact_dir, 'best.pt')

                os.system(f'cp {trained_model_path} {final_path}')

                logger.info(f'Model saved at {final_path}')

            else:
                logger.warning('Best model not found')

        except Exception as e:
            raise CustomException(e, sys)