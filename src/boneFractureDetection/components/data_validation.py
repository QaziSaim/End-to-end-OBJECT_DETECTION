import os
import sys
from pathlib import Path

from src.boneFractureDetection.logging.logger import logger
from src.boneFractureDetection.exception.exception import CustomException

class DataValidation:
    def __init__(self, data_path:str):
        self.data_path = data_path

    
    def validate_structure(self):
        try:
            logger.info("Checking dataset folder structure")

            required_folder = ['train','test','valid']

            for folder in required_folder:
                folder_path = os.path.join(self.data_path, folder)

                if not os.path.exists(folder_path):
                    raise Exception(f'Missing folder: {folder}')
                if not os.path.exists(os.path.join(folder_path,'images')):
                    raise Exception(f'Missing images folder in {folder}')
                if not os.path.exists(os.path.join(folder_path,'labels')):
                    raise Exception(f'Missing labels folder in {folder}')
            
            logger.info('Dataset structure validation passed ')
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def validate_images_labels_counts(self):
        try:
            logger.info('Checking image-label count consistency...')

            for split in ['train','test','valid']:
                img_path = os.path.join(self.data_path, split, 'images')
                lbl_path = os.path.join(self.data_path, split, 'labels')

                images = os.listdir(img_path)
                labels = os.listdir(lbl_path)

                if len(images) != len(labels):
                    logger.warning(
                        f'{split}: Mismatch -> Images {len(images)}, Labels: {len(labels)}'
                    )
                else:
                    logger.info(f'{split}: Image-label count matched')
        except Exception as e:
            raise CustomException(e, sys)
    
    