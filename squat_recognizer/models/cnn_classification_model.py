"Cnn ClassificationModel class."

from typing import Dict, Callable, Optional, Type, List, Tuple

from torch.nn import Module
from fastai.vision import cnn_learner, Learner, error_rate, load_learner, Image
from fastai.vision.models import resnet34
from torchsummary import summary
from torchsummary.model_statistics import ModelStatistics

from squat_recognizer.datasets.fvbs_dataset import FvbsDataset
from squat_recognizer.datasets.dataset import Dataset
from .base import Model


class CnnClassificationModel(Model):
    """Simple classification model."""

    def __init__(
        self,
        dataset_cls: Type[Dataset] = FvbsDataset,
        learner_fn: Callable[..., Learner] = cnn_learner,
        network_fn: Callable[..., Module] = resnet34,
        dataset_args: Optional[Dict] = None,
    ):

        super().__init__(dataset_cls, network_fn)

        if dataset_args is None:
            dataset_args = {}

        self.dataset = FvbsDataset(**dataset_args)
        self.learner_fn = learner_fn
        self.learner: Learner = None

    def fit(self, stage_one: Dict, stage_two: Optional[Dict] = None, save_weights: bool = False) -> None:
        """Fits a learner to the databunch given the training specs"""
        self.dataset.load_or_generate_data()
        self.learner = self.learner_fn(self.dataset.databunch, self.network_fn, metrics=error_rate)

        # Stage one of training.
        s1_epochs: int = stage_one["epochs"]
        s1_one_cycle: int = stage_one["one_cycle"]

        if s1_one_cycle == 1:
            self.learner.fit_one_cycle(s1_epochs)
        else:
            self.learner.fit(s1_epochs)

        if save_weights:
            self.save_weights("stage-1")

        if stage_two is None:
            return

        # Stage two of training.
        s2_unfreeze: int = stage_two["unfreeze"]
        s2_epochs: int = stage_two["epochs"]
        s2_one_cycle: int = stage_two["one_cycle"]
        s2_max_lr_start = float(stage_two["max_lr_start"])
        s2_max_lr_end = float(stage_two["max_lr_end"])

        lr_slice = slice(s2_max_lr_start, s2_max_lr_end)

        if s2_unfreeze == 1:
            self.learner.unfreeze()

        if s2_one_cycle == 1:
            self.learner.fit_one_cycle(s2_epochs, max_lr=lr_slice)
        else:
            self.learner.fit(s2_epochs, max_lr=lr_slice)

        if save_weights:
            self.save_weights("stage-2")

    def predict(self, obj: Image) -> Tuple[str, float]:
        if self.learner is None:
            raise ValueError("Error: Load or train model first ...")
        pred, pred_idx, outputs = self.learner.predict(obj)
        return (pred.obj, outputs[pred_idx])

    def save_weights(self, stage: str) -> None:
        if self.learner is None:
            raise ValueError("Error: Cannot save weights. Learner is None...")
        self.learner.save(self.weights_filename(stage))

    def load_weights(self, stage: str) -> None:
        if self.learner is None:
            raise ValueError("Error: Cannot load weights. Learner is None...")
        self.learner.load(self.weights_filename(stage))

    def export(self) -> None:
        if self.learner is None:
            raise ValueError("Error: Cannot export model. Learner is None...")
        self.learner.export(self.export_filename)

    def load_export(self) -> None:
        self.learner = load_learner(self.export_dirname, f"{self.name}.pkl")

    @property
    def image_shape(self) -> List:
        return self.dataset.input_shape

    def __repr__(self) -> str:
        if self.learner is None:
            raise ValueError("Error: Cannot represent model. Learner is None...")
        model_stats: ModelStatistics = summary(self.learner.model)
        return model_stats.__repr__()
