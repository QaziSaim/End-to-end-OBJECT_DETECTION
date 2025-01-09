import os
from dotenv import load_dotenv
ARTIFACTS_DIR: str = "artifacts"

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

# DATA_DOWNLOAD_URL: str = "https://github.com/QaziSaim/End-to-end-OBJECT_DETECTION/raw/refs/heads/main/object_detection/data/Dataset.zip"
# DATA_DOWNLOAD_URL: str = "https://github.com/QaziSaim/Bike-Rental-Demand-Prediction-/raw/refs/heads/main/Thermal_Dogs_and_People.zip"

DATA_DOWNLOAD_URL: str = "https://github.com/entbappy/Branching-tutorial/raw/master/Sign_language_data.zip"


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_STATUS_FILE = 'status.txt'

DATA_VALIDATION_ALL_REQUIRED_FILES = ["test", "train", "valid","data.yaml"]
# DATA_VALIDATION_ALL_REQUIRED_FILES = ["object_dataset"]



"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
# """
MODEL_TRAINER_DIR_NAME: str = "model_trainer"

MODEL_TRAINER_PRETRAINED_WEIGHT_NAME: str = "yolov5s.pt"

MODEL_TRAINER_NO_EPOCHS: int = 1

MODEL_TRAINER_BATCH_SIZE: int = 16




"""
MODEL PUSHER related constant start with MODEL_PUSHER var name
"""
BUCKET_NAME = "object-detection-sahim"
S3_MODEL_NAME = "best.pt"

AWS_DEFAULT_REGION=os.getenv('AWS_DEFAULT_REGION')
AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')

