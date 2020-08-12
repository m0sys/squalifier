"Cnn ClassificationModel class."

from pathlib import Path
from typing import Union, Dict, Callable
from torchsummary import summary

from fastai.vision import cnn_learner, Learner
from fastai.vision.models import resnet34

from .base import Model
from squat_recognizer.datasets.fvbs_dataset import FvbsDataset

from torch.nn import Module

class CnnClassificationModel(Model):
  """Simple classification model."""

  def __init__(
    self, 
    dataset_cls: type = FvbsDataset, 
    learner_fn: Callable[..., Learner] = cnn_learner,
    network_fn: Callable[..., Module] = resnet34,
    dataset_args: Dict = None):

    super().__init__(dataset_cls, learner_fn, network_fn,
                     dataset_args)