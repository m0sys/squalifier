"""Function to train a model."""

from time import time
from typing import Dict

from squat_recognizer.models.base import Model


def train_model(model: Model, stage_one: Dict, stage_two: Dict, save_weights: bool,) -> None:
    t = time()
    model.fit(stage_one, stage_two, save_weights)
    print("Training took {:2f} s".format(time() - t))
