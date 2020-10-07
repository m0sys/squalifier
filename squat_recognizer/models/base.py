"""Model class, to be extended by specific types of models."""
import os
from pathlib import Path
from typing import Callable, Dict, Type, Tuple, Optional

from fastai.vision import Image
from torch.nn import Module

from squat_recognizer.datasets.dataset import Dataset
from squat_recognizer import utils

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

    def save_weights(self, stage: str) -> None:
        raise NotImplementedError

    def load_weights(self, stage: str) -> None:
        raise NotImplementedError

    def export(self) -> None:
        raise NotImplementedError

    def load_export(self) -> None:
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

    @classmethod
    def export_dirname(cls) -> Path:
        return EXPORT_DIRNAME

    def __repr__(self) -> str:
        raise NotImplementedError


def _download_exported_model_from_s3(metadata) -> None:
    if os.path.exists(metadata["filename"]):
        return
    print(f"Downloading exported model from {metadata['bucket']}/{metadata['object']}...")
    utils.download_object_from_s3(metadata["bucket"], metadata["object"], metadata["filename"])
    print("Computing SHA-256...")
    sha256 = utils.compute_sha256(metadata["filename"])
    if sha256 != metadata["sha256"]:
        raise ValueError("Downloaded model file SHA-256 does not match that listed in metadata document.")
