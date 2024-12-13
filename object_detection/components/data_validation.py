import os, sys
import shutil # we can check any type of directory and copy or move any type of directory
from object_detection.logger.logger import logging
from object_detection.exception.exception import CustomException
from object_detection.entity.config_entity import DataValidationConfig
from object_detection.entity.artifacts_entity import (DataIngestionArtifact,
                                                  DataValidationArtifact)

import zipfile

class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise CustomException(e, sys) 
        

    
    def validate_all_files_exist(self) -> bool:
        try:
            
            validation_status = "i am going to write file path"
            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            for sub_file in all_files:
                logging.info(f"types of file {sub_file}")
                if os.path.isdir(sub_file):
                    logging.info(f"type of file {file}")
                    # logging.info(f"{sub_file} is a folder.")
                    for file in os.listdir(sub_file):
                        # logging.info(f"files are {file}")
                        if file not in self.data_validation_config.required_file_list:
                            validation_status = False
                            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                            with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                                f.write(f"Validation status: {validation_status}")
                        else:
                            validation_status = True
                            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                            with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                                f.write(f"Validation status: {validation_status}")
            return validation_status
                # if os.path.isdir(file):
                #     logging.info(f"{file} is a folder.")
                #     for item in os.listdir(file):
                #         item_path=os.path.join(file,item)
                #         if os.path.isfile(item_path):
                #             logging.info(f"File {item}")
                #         elif os.path.isdir(item_path):
                #             logging.info(f"Folder {item}")
                # # Check if it's a ZIP file
                # elif os.path.isfile(file) and zipfile.is_zipfile(file):
                #     logging.info(f"{file} is a ZIP file.")
                # else:
                #     logging.info(f"{file} is neither a folder nor a valid ZIP file.")
                

                
            

        except Exception as e:
            raise CustomException(e, sys)
        

    
    def initiate_data_validation(self) -> DataValidationArtifact: 
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status)

            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)