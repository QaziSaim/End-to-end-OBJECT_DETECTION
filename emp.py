import sys, os, posixpath
from object_detection.pipeline.training_pipeline import TrainPipeline
from object_detection.exception.exception import CustomException
from object_detection.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin
import shutil  # For removing directories


app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return "Training Successful!!"


@app.route("/predict", methods=['POST', 'GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)

        # Use posixpath to build paths
        yolov5_path = posixpath.join("yolov5")
        detect_script = posixpath.join(yolov5_path, "detect.py")
        input_image = posixpath.join("..", "data", "inputImage.jpg")
        runs_path = posixpath.join(yolov5_path, "runs")
        result_image = posixpath.join(runs_path, "detect", "exp", "inputImage.jpg")

        os.system(f"cd {yolov5_path} && python {detect_script} --weights best.pt --img 416 --conf 0.5 --source {input_image}")

        opencodedbase64 = encodeImageIntoBase64(result_image)
        result = {"image": opencodedbase64.decode('utf-8')}

        # Remove the runs directory
        if os.path.exists(runs_path):
            shutil.rmtree(runs_path)

    except ValueError as val:
        print(val)
        return Response("Value not found inside JSON data")
    except KeyError:
        return Response("Key value error: incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)


@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        # Use posixpath to build paths
        yolov5_path = posixpath.join("yolov5")
        detect_script = posixpath.join(yolov5_path, "detect.py")
        runs_path = posixpath.join(yolov5_path, "runs")

        os.system(f"cd {yolov5_path} && python {detect_script} --weights best.pt --img 416 --conf 0.5 --source 0")
        
        # Remove the runs directory
        if os.path.exists(runs_path):
            shutil.rmtree(runs_path)

        return "Camera starting!!"

    except ValueError as val:
        print(val)
        return Response("Value not found inside JSON data")


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=8080)

