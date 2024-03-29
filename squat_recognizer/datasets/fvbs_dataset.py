"""
Front VS Back Squat Dataset (fvbs). Download from s3 bucket and saves as
.npz file if not already present.
"""

import json
import os
from pathlib import Path
import shutil
from typing import Union, List, Optional, MutableMapping, Any

import numpy as np
import toml

from fastai.vision import ImageDataBunch, get_transforms, imagenet_stats, ImageList, LabelLists, LabelList

from squat_recognizer.datasets.dataset import (
    _download_raw_dataset_from_s3,
    _extract_raw_dataset,
    Dataset,
)

SAMPLE_TO_BALANCE = False  # if true, take at most the mean number of instances per class.

RAW_DATA_DIRNAME = Dataset.data_dirname() / "raw" / "fvbs"
METADATA_FILENAME = RAW_DATA_DIRNAME / "metadata.toml"

EXTRACTED_DATASET_DIRNAME = RAW_DATA_DIRNAME / "fvbs_dataset"

PROCESSED_DATA_DIRNAME = Dataset.data_dirname() / "processed" / "fvbs"
PROCESSED_DATA_VALID_DIRNAME = PROCESSED_DATA_DIRNAME / "valid"
PROCESSED_DATA_TRAIN_DIRNAME = PROCESSED_DATA_DIRNAME / "train"

ESSENTIAL_FILENAME = Path(__file__).parents[0].resolve() / "fvbs_essentials.json"


class FvbsDataset(Dataset):
    """
    This dataset contains about 800 images of different people assuming front squat or back squat positions.
    More specifically there are about 400 images of people or diagrams performing front squats and 400 images
    of people or diagrams performing back squats.

    The labels consist of the directory each image is in. If an image is in the back-squat directory then it is
    labeled as 'back-squat'. If an image is in the front-squat directory then it is labeled as 'front-squat'
    """

    def __init__(self, image_size: int = 224, subsample_fraction: float = None):
        super().__init__()
        self.image_size: int = image_size
        self.subsample_fraction: Optional[float] = subsample_fraction
        self.metadata: MutableMapping[str, Any] = toml.load(METADATA_FILENAME)
        self.random_seed = 42

        if not os.path.exists(ESSENTIAL_FILENAME):
            self._download_and_process_fvbs()

        with open(ESSENTIAL_FILENAME) as f:
            essentials = json.load(f)

        self.classes = list(essentials["classes"])
        self.input_shape: List = essentials["input_shape"]
        self.output_shape = len(self.classes)

        self.databunch: Optional[ImageDataBunch] = None

    def load_or_generate_data(self) -> None:
        if not os.path.exists(PROCESSED_DATA_DIRNAME):
            self._download_and_process_fvbs()

        path: Path = PROCESSED_DATA_DIRNAME
        src: LabelLists = ImageList.from_folder(path).split_by_folder().label_from_folder()
        self.databunch = src.transform(get_transforms(), size=self.input_shape[1]).databunch().normalize(imagenet_stats)

    @classmethod
    def essential_dirname(cls) -> Path:
        return ESSENTIAL_FILENAME

    def _download_and_process_fvbs(self) -> None:
        root_dir: Union[Path, str] = self._download_fvbs_dataset()
        self._extract_fvbs_dataset(root_dir)
        data: ImageDataBunch = self._process_fvbs_dataset()
        _save_essential_dataset_params(data)
        _clean_up()

    def _download_fvbs_dataset(self) -> Union[Path, str]:
        root_dir: Union[Path, str] = os.getcwd()
        os.chdir(RAW_DATA_DIRNAME)
        _download_raw_dataset_from_s3(self.metadata)
        return root_dir

    def _extract_fvbs_dataset(self, root_dir: Union[Path, str]):
        if not EXTRACTED_DATASET_DIRNAME.exists():
            EXTRACTED_DATASET_DIRNAME.mkdir(parents=True, exist_ok=True)
        _extract_raw_dataset(self.metadata, EXTRACTED_DATASET_DIRNAME)
        os.chdir(root_dir)

    def _process_fvbs_dataset(self) -> ImageDataBunch:
        np.random.seed(self.random_seed)
        path: Path = EXTRACTED_DATASET_DIRNAME / "front_vs_back_dataset" / "preprocessed"
        src: LabelLists = ImageList.from_folder(path).split_by_rand_pct(0.2).label_from_folder()

        train_item_list: LabelList = src.train
        valid_item_list: LabelList = src.valid

        PROCESSED_DATA_DIRNAME.mkdir(parents=True, exist_ok=True)
        PROCESSED_DATA_TRAIN_DIRNAME.mkdir(parents=True, exist_ok=True)
        PROCESSED_DATA_VALID_DIRNAME.mkdir(parents=True, exist_ok=True)

        (PROCESSED_DATA_TRAIN_DIRNAME / "back-squat").mkdir(parents=True, exist_ok=True)
        (PROCESSED_DATA_TRAIN_DIRNAME / "front-squat").mkdir(parents=True, exist_ok=True)

        (PROCESSED_DATA_VALID_DIRNAME / "back-squat").mkdir(parents=True, exist_ok=True)
        (PROCESSED_DATA_VALID_DIRNAME / "front-squat").mkdir(parents=True, exist_ok=True)

        _sort_images_into_categories(train_item_list, PROCESSED_DATA_TRAIN_DIRNAME)
        _sort_images_into_categories(valid_item_list, PROCESSED_DATA_VALID_DIRNAME)

        data: ImageDataBunch = (
            src.transform(get_transforms(), size=self.image_size).databunch().normalize(imagenet_stats)
        )

        return data

    def __repr__(self):
        return self.databunch.__repr__


def _sort_images_into_categories(items: LabelList, path: Path):
    for i, item in enumerate(items):
        object_path: Path = items.x.items[i]
        if item[1].obj == "back-squat":
            shutil.copy(object_path, path / "back-squat")

        elif item[1].obj == "front-squat":
            shutil.copy(object_path, path / "front-squat")


def _save_essential_dataset_params(data: ImageDataBunch) -> None:
    """
Save essential dataset parameters in a .json file at a canonical location
(See `ESSENTIAL_FILENAME` above).
"""
    print("Saving essential dataset parameters to squat_recognizer/datasets...")

    essentials = {
        "classes": data.classes,
        "input_shape": list(data.train_ds[0][0].shape),
    }

    with open(ESSENTIAL_FILENAME, "w") as f:
        json.dump(essentials, f)


def _clean_up():
    print("Cleaning up...")
    root_dir: Union[Path, str] = os.getcwd()
    os.chdir(RAW_DATA_DIRNAME)
    shutil.rmtree("fvbs_dataset")
    os.chdir(root_dir)
