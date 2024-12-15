import os
import sys
# import logenv
from dotenv import load_dotenv
from io import StringIO
from typing import List, Union
from object_detection.constant import *
import boto3
import pickle
from object_detection.exception.exception import CustomException
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket
from pandas import DataFrame, read_csv
from object_detection.logger.logger import logging

# Load environment variables from .env file
load_dotenv()

class S3Operation:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'ap-south-1')  # Default region if not set
        )
        self.s3_resource = boto3.resource(
            service_name='s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'ap-south-1')  # Default region
        )

    @staticmethod
    def read_object(
        object_name: str, decode: bool = True, make_readable: bool = False
    ) -> Union[StringIO, str]:
        logging.info("Entered the read_object method of S3Operations class")
        try:
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )
            conv_func = lambda: StringIO(func()) if make_readable is True else func()
            logging.info("Exited the read_object method of S3Operations class")
            return conv_func()
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_bucket(self, bucket_name: str) -> Bucket:
        logging.info("Entered the get_bucket method of S3Operations class")
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of S3Operations class")
            return bucket
        except Exception as e:
            raise CustomException(e, sys) from e

    def is_model_present(self, bucket_name: str, s3_model_key: str) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [
                file_object
                for file_object in bucket.objects.filter(Prefix=s3_model_key)
            ]
            return len(file_objects) > 0
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_file_object(
        self, filename: str, bucket_name: str
    ) -> Union[List[object], object]:
        logging.info("Entered the get_file_object method of S3Operations class")
        try:
            bucket = self.get_bucket(bucket_name)
            lst_objs = [object for object in bucket.objects.filter(Prefix=filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(lst_objs)
            logging.info("Exited the get_file_object method of S3Operations class")
            return file_objs
        except Exception as e:
            raise CustomException(e, sys) from e

    def load_model(
        self, model_name: str, bucket_name: str, model_dir: str = None
    ) -> object:
        logging.info("Entered the load_model method of S3Operations class")
        try:
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )
            model_file = func()
            f_obj = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(f_obj, decode=False)
            model = pickle.loads(model_obj)
            logging.info("Exited the load_model method of S3Operations class")
            return model
        except Exception as e:
            raise CustomException(e, sys) from e

    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True,
    ) -> None:
        logging.info("Entered the upload_file method of S3Operations class")
        try:
            logging.info(
                f"Uploading {from_filename} to {to_filename} in {bucket_name} bucket"
            )
            self.s3_resource.Bucket(bucket_name).upload_file(
                from_filename, to_filename
            )
            logging.info(f"Uploaded {from_filename} to {to_filename}")
            if remove:
                os.remove(from_filename)
                logging.info(f"File {from_filename} deleted after upload")
        except Exception as e:
            raise CustomException(e, sys) from e

    # Other methods remain unchanged...
