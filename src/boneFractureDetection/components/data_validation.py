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
    
    def check_missing_labels(self):
        try:
            logger.info('Checking missing labels...')

            for split in ['train','test','valid']:
                img_path = os.path.join(self.data_path,split,'images')
                lbl_path = os.path.join(self.data_path,split,'labels')

                images = os.listdir(img_path)
                labels = os.listdir(lbl_path)

                label_set = set(labels)
                for img in images:
                    label_name = (
                        img.replace('.jpg','.txt').replace('.png','.txt').replace('.jpeg','.txt')

                    )

                    if label_name not in label_set:
                        logger.warning(f'Missing label for image {img}')
            logger.info('Missing label check completed')
        except Exception as e:
            raise CustomException(e, sys)

    def check_empty_files(self):
        try:
            logger.info('Checking for empty labels files...')

            for split in ['train','test','valid']:
                lbl_path = os.path.join(self.data_path, split, 'labels')

                for file in os.listdir(lbl_path):
                    file_path = os.path.join(lbl_path, file)

                    if os.path.getsize(file_path) == 0:
                        logger.warning(f'Empty label files: {file_path}')   
        except Exception as e:
            raise CustomException(e, sys)
    
    def run_validation(self):
        try:
            logger.info('Starting Data Validation Pipeline...')

            self.validate_structure()
            self.validate_images_labels_counts()
            self.check_missing_labels()
            self.check_empty_files()

            logger.info('Data Validation Completed Successfully')
        
        except Exception as e:
            raise CustomException(e, sys)

    
