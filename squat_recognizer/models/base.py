"""Model class, to be extended by specific types of models."""
from pathlib import Path
from typing import Callable, Dict, Type, Tuple, Optional

from fastai.vision import Image
from torch.nn import Module

from squat_recognizer.datasets.dataset import Dataset

DIRNAME = Path(__file__).parents[1].resolve() / "weights"
EXPORT_DIRNAME = Path(__file__).parents[1].resolve() / "exports"


class Model:
    """Base model class, to be subclassed by predictors for specific type of data."""

    def __init__(self, dataset_cls: Type[Dataset], network_fn: Callable[..., Module]):
        self.network_fn: Callable[..., Module] = network_fn
        self.name = f"{self.__class__.__name__}_{dataset_cls.__name__}_{network_fn.__name__}"

    def fit(self, stage_one: Dict, stage_two: Optional[Dict], save_weights: bool = False) -> None:
        raise NotImplementedError

    def predict(self, obj: Image) -> Tuple[str, float]:
        raise NotImplementedError

    def export(self) -> None:
        raise NotImplementedError

    def weights_filename(self, stage: str) -> str:
        DIRNAME.mkdir(parents=True, exist_ok=True)
        return str(DIRNAME / f"{self.name}_weights_{stage}")

    @property
    def weights_dirname(self) -> Path:
        return DIRNAME

    @property
    def export_filename(self) -> str:
        EXPORT_DIRNAME.mkdir(parents=True, exist_ok=True)
        return str(EXPORT_DIRNAME / f"{self.name}.pkl")

    @property
    def export_dirname(self) -> Path:
        return EXPORT_DIRNAME

    def __repr__(self) -> str:
        raise NotImplementedError
