"""Model class, to be extended by specific types of models."""
from pathlib import Path
from typing import Callable, Dict, List, Optional

from fastai.vision import Learner, error_rate
from torch.nn import Module
from torchsummary import summary
from torchsummary.model_statistics import ModelStatistics

from squat_recognizer.datasets.dataset import Dataset

DIRNAME = Path(__file__).parents[1].resolve() / "weights"
EXPORT_DIRNAME = Path(__file__).parents[1].resolve() / "exports"


class Model:
    """Base class, to be subclassed by predictors for specific type of data."""

    def __init__(
        self,
        dataset_cls: Dataset,
        network_fn: Callable[..., Module],
        learner_fn: Callable[..., Learner],
        dataset_args: Optional[Dict] = None,
    ):

        self.network_fn: Callable[..., Module] = network_fn
        self.learner_fn: Callable[..., Learner] = learner_fn

        self.name = f"{self.__class__.__name__}_{dataset_cls.__name__}_{network_fn.__name__}"

        if dataset_args is None:
            dataset_args = {}
        self.dataset: Dataset = dataset_cls(**dataset_args)

        self.learner: Optional[Learner] = None

    @property
    def image_shape(self) -> List:
        return self.dataset.input_shape

    def weights_filename(self, stage: str) -> str:
        DIRNAME.mkdir(parents=True, exist_ok=True)
        return str(DIRNAME / f"{self.name}_weights_{stage}")

    @property
    def export_filename(self) -> str:
        EXPORT_DIRNAME.mkdir(parents=True, exist_ok=True)
        return str(EXPORT_DIRNAME / f"{self.name}.pkl")

    def fit(self, stage_one: Dict, stage_two: Dict = None, save_weights: bool = False) -> None:
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

    def __repr__(self) -> str:
        if self.learner is None:
            raise ValueError("Error: Cannot represent model. Learner is None...")
        model_stats: ModelStatistics = summary(self.learner.model)
        return model_stats.__repr__()
