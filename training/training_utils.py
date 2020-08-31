"""Function to train a model."""

from time import time
from typing import Dict

from fastai.vision import DataBunch, Learner

from squat_recognizer.models.base import Model


def train_model(model: Model, databunch: DataBunch, stage_one: Dict, stage_two: Dict, save_weights: bool,) -> Learner:
    t = time()
    learner = model.fit(databunch, stage_one, stage_two, save_weights)
    print("Training took {:2f} s".format(time() - t))

    return learner
