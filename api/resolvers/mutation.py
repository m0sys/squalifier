"""Root GraphQL mutation for making predictions."""
from io import BytesIO
from ariadne import convert_kwargs_to_snake_case, MutationType
from fastapi import UploadFile, File
from fastai.vision import open_image, Image

from squat_recognizer.squat_recognizer import SquatRecognizer

mutation = MutationType()


@mutation.field("makePrediction")
@convert_kwargs_to_snake_case
async def resolve_make_prediction(*_, image: UploadFile = File(...)):
    predictor = SquatRecognizer()
    contents = await image.read()
    img: Image = open_image(BytesIO(contents))
    pred, conf = predictor.predict(img)
    return {"prediction": pred, "confidence": conf}
