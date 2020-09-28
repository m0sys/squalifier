"""FastAPI web server servince squat_recognizer predictions."""
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from fastai.vision import open_image, Image
import uvicorn

from squat_recognizer.squat_recognizer import SquatRecognizer


app = FastAPI()


@app.get("/")
def read_main():
    return {"msg": "Hello World!"}


@app.post("/v1/predict")
async def predict_route(file: UploadFile = File(...)):
    predictor = SquatRecognizer()
    contents = await file.read()
    img: Image = open_image(BytesIO(contents))
    pred, _ = predictor.predict(img)
    return {"pred": pred}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
