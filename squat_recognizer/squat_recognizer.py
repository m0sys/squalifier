"""The official Front vs Back squat recognizer."""

from typing import Optional, Tuple, Union
from fastai.vision import Image

from squat_recognizer.models.cnn_classification_model import CnnClassificationModel


class SquatRecognizer:
    """A Front vs Back squat recognizer ready for inference."""

    def __init__(self) -> None:
        self.model = CnnClassificationModel()
        self.model.load_export()

    def predict(self, img: Optional[Image] = None) -> Union[Tuple[str, float], str]:
        if img is None:
            return "no image given"
        return self.model.predict(img)
