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


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            # Unzip the dataset
            logging.info("Unzipping data")
            with zipfile.ZipFile('Thermal_Dogs_and_People.zip', 'r') as zip_ref:
                zip_ref.extractall('.')
            os.remove('Thermal_Dogs_and_People.zip')

            # Read the number of classes
            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            logging.info(f"Model config file name: {model_config_file_name}")

            # Update YOLOv5 model configuration
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)
            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            # Train the model
            logging.info("Starting YOLOv5 training")
            import subprocess
            subprocess.run(["python", "train.py", "--img", "416",
                            "--batch", str(self.model_trainer_config.batch_size),
                            "--epochs", str(self.model_trainer_config.no_epochs),
                            "--data", "../data.yaml",
                            "--cfg", f"./models/custom_{model_config_file_name}.yaml",
                            "--weights", self.model_trainer_config.weight_name,
                            "--name", "yolov5s_results",
                            "--cache"], cwd="yolov5/")

            # Copy trained model
            logging.info("Copying trained model")
            trained_model_path = "yolov5/runs/train/yolov5s_results/weights/best.pt"
            shutil.copy(trained_model_path, "yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            shutil.copy(trained_model_path, self.model_trainer_config.model_trainer_dir)

            # Cleanup
            shutil.rmtree("yolov5/runs", ignore_errors=True)
            os.remove("data.yaml")

            # Create artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
