import os,sys
import yaml
from object_detection.utils.main_utils import read_yaml_file
from object_detection.logger.logger import logging
from object_detection.exception.exception import CustomException
from object_detection.entity.config_entity import ModelTrainerConfig
from object_detection.entity.artifacts_entity import ModelTrainerArtifact
import zipfile
import shutil
class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.model_trainer_config = model_trainer_config


    
    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")

            with zipfile.ZipFile("object_dataset.zip","r") as zip_ref:
                zip_ref.extractall(".")
            os.remove("object_dataset.zip")
            if not os.path.exists("data.yaml"):
                raise FileNotFoundError("data.yaml file not found after extraction.")
            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)

            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")

            config['nc'] = int(num_classes)


            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} "
              f"--epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg "
              f"./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} "
              f"--name yolov5s_results --cache")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            shutil.copy("yolov5/runs/train/yolov5s_results/weights/best.pt", self.model_trainer_config.model_trainer_dir)

            # Clean up
            shutil.rmtree("yolov5/runs", ignore_errors=True)
            os.remove("data.yaml")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)


