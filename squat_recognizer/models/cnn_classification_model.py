"Cnn ClassificationModel class."

from typing import Dict, Callable, Optional

from torch.nn import Module
from fastai.vision import cnn_learner, Learner
from fastai.vision.models import resnet34

from squat_recognizer.datasets.fvbs_dataset import FvbsDataset
from squat_recognizer.datasets.dataset import Dataset
from .base import Model


class CnnClassificationModel(Model):
    """Simple classification model."""

    def __init__(
        self,
        dataset_cls: Dataset = FvbsDataset,
        learner_fn: Callable[..., Learner] = cnn_learner,
        network_fn: Callable[..., Module] = resnet34,
        dataset_args: Optional[Dict] = None,
    ):

        super().__init__(dataset_cls, network_fn, learner_fn, dataset_args)
