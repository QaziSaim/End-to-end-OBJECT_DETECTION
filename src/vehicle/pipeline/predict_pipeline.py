from src.vehicle.pipeline.predict_pipeline import PredictPipeline

pipeline = PredictPipeline()

output, result = pipeline.predict("test.jpg")

pipeline.save_json(output)
pipeline.save_image(result)

print(output)