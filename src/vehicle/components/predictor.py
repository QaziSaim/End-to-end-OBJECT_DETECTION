import os
import sys
import cv2
import json

from ultralytics import YOLO
from src.vehicle.logging.logger import logger
from src.vehicle.exception.exception import CustomException


class PredictPipeline:
    def __init__(self, model_path: str = "artifact/model/best.pt"):
        self.model_path = model_path

    def load_model(self):
        try:
            logger.info("Loading trained model...")
            model = YOLO(self.model_path)
            return model
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, image_path: str):
        try:
            logger.info(f"Running prediction on {image_path}")

            model = self.load_model()

            # Read image
            image = cv2.imread(image_path)

            results = model(image, conf=0.25)

            result = results[0]

            output = []

            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                label = model.names[cls]

                output.append({
                    "label": label,
                    "confidence": round(conf, 2),
                    "bbox": [x1, y1, x2, y2]
                })

            logger.info("Prediction completed successfully")

            return output, result

        except Exception as e:
            raise CustomException(e, sys)

    def save_json(self, output, save_path="artifact/predictions/output.json"):
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, "w") as f:
                json.dump(output, f, indent=4)

            logger.info(f"JSON saved at {save_path}")

        except Exception as e:
            raise CustomException(e, sys)

    def save_image(self, result, save_path="artifact/predictions/output.jpg"):
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            plotted = result.plot()
            cv2.imwrite(save_path, plotted)

            logger.info(f"Image saved at {save_path}")

        except Exception as e:
            raise CustomException(e, sys)