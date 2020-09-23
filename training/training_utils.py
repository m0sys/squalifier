"""Function to train a model."""

import importlib
from time import time
from typing import Dict, Type

from squat_recognizer.models.base import Model


def train_model(model: Model, stage_one: Dict, stage_two: Dict, save_weights: bool,) -> None:
    t = time()
    model.fit(stage_one, stage_two, save_weights)
    print("Training took {:2f} s".format(time() - t))


def load_model_from_weights(weight_name: str) -> Model:
    """
    Loads model from canonical weight directory.

    Preconditions:
        weight_name: must be in the following format:

                     MODEL_DATASET_NETWORK_weights_STAGE.pth

                     Where MODEL is the class name for the model used
                     to train the weights,
                     DATASET is the dataset that MODEL was trained on,
                     NETWORK is the subnet used in MODEL's architecture,
                     and STAGE is the stage of the weight {'stage-1', 'stage-2'}
    """
    specs = weight_name.split("_")
    weight_specs = {"model": specs[0], "dataset": specs[1], "network": specs[2], "stage": specs[4][:-4]}

    datasets_module = importlib.import_module("squat_recognizer.datasets")
    dataset_class_ = getattr(datasets_module, weight_specs["dataset"])

    network_module = importlib.import_module("fastai.vision.models")
    network_fn_ = getattr(network_module, weight_specs["network"])

    models_module = importlib.import_module("squat_recognizer.models")
    model_class_: Type[Model] = getattr(models_module, weight_specs["model"])

    model = model_class_(dataset_class_, network_fn=network_fn_)
    model.load_weights(weight_specs["stage"])

    return model


def export_model_from_weights(weight_name: str) -> None:
    """Export's model weights to a canonical export directory."""
    model = load_model_from_weights(weight_name)

    model.export()
