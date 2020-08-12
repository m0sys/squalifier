"""
Front VS Back Squat Dataset (fvbs). Download from s3 bucket and saves as
.npz file if not already present.
"""

import json
import os
from pathlib import Path
import shutil
from typing import List, Dict, Union

from boltons.cacheutils import cachedproperty
import h5py
import numpy as np
import toml

from fastai.vision import ImageDataBunch, get_transforms, imagenet_stats, ImageList

from squat_recognizer.datasets.dataset import _download_raw_dataset_from_s3, _extract_raw_dataset, Dataset, _parse_args

SAMPLE_TO_BALANCE = False # if true, take at most the mean number of instances per class.

RAW_DATA_DIRNAME = Dataset.data_dirname() / "raw" / "fvbs"
METADATA_FILENAME = RAW_DATA_DIRNAME / "metadata.toml"

EXTRACTED_DATASET_DIRNAME = RAW_DATA_DIRNAME / "fvbs_dataset"

PROCESSED_DATA_DIRNAME = Dataset.data_dirname() / "processed" / "fvbs"
## PROCESSED_DATA_FILENAME = PROCESSED_DATA_DIRNAME / "image_data_bunch.h5"
PROCESSED_DATA_VALID_DIRNAME = PROCESSED_DATA_DIRNAME / 'valid'
PROCESSED_DATA_TRAIN_DIRNAME = PROCESSED_DATA_DIRNAME / 'train'

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
    self.image_size = image_size
    self.subsample_fraction = subsample_fraction
    self.metadata = toml.load(METADATA_FILENAME)
    self.random_seed = 42

    if not os.path.exists(ESSENTIAL_FILENAME):
      self._download_and_process_fvbs()
    
    with open(ESSENTIAL_FILENAME) as f:
      essentials = json.load(f)

    self.classes = list(essentials["classes"])
    self.input_shape = essentials["input_shape"]
    self.output_shape = len(self.classes)

    self.data = None

  def load_or_generate_data(self) -> None:
    if not os.path.exists(PROCESSED_DATA_DIRNAME):
      self._download_and_process_fvbs()
    
    ## with h5py.File(PROCESSED_DATA_FILENAME, "r") as f:
    ##   data = f["data"]
    path = (PROCESSED_DATA_DIRNAME)
    src = (ImageList.from_folder(path)
           .split_by_folder()
           .label_from_folder())
    self.data = (src.transform(get_transforms(), size=self.input_shape[1])
                 .databunch().normalize(imagenet_stats))

  def _download_and_process_fvbs(self) -> None:
    root_dir = self._download_fvbs_dataset()
    self._extract_fvbs_dataset(root_dir)
    data = self._process_fvbs_dataset()
    ## self._save_processed_fvbs_dataset(data)
    self._save_essential_dataset_params(data)
    self._clean_up()

  def _download_fvbs_dataset(self) -> Union[Path, str]:
    root_dir = os.getcwd()
    os.chdir(RAW_DATA_DIRNAME)
    _download_raw_dataset_from_s3(self.metadata)
    return root_dir

  def _extract_fvbs_dataset(self, root_dir: str):
    if not EXTRACTED_DATASET_DIRNAME.exists():
      EXTRACTED_DATASET_DIRNAME.mkdir(parents=True, exist_ok=True)
    _extract_raw_dataset(self.metadata, EXTRACTED_DATASET_DIRNAME)
    os.chdir(root_dir)

  def _process_fvbs_dataset(self) -> None:
    np.random.seed(self.random_seed)
    path = EXTRACTED_DATASET_DIRNAME / 'front_vs_back_dataset' / 'preprocessed'
    src = (ImageList.from_folder(path)
            .split_by_rand_pct(0.2)
            .label_from_folder())

    train_item_list = src.train
    valid_item_list = src.valid


    PROCESSED_DATA_DIRNAME.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_TRAIN_DIRNAME.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_VALID_DIRNAME.mkdir(parents=True, exist_ok=True)

    (PROCESSED_DATA_TRAIN_DIRNAME / 'back-squat').mkdir(parents=True, exist_ok=True)
    (PROCESSED_DATA_TRAIN_DIRNAME / 'front-squat').mkdir(parents=True, exist_ok=True)

    (PROCESSED_DATA_VALID_DIRNAME / 'back-squat').mkdir(parents=True, exist_ok=True)
    (PROCESSED_DATA_VALID_DIRNAME / 'front-squat').mkdir(parents=True, exist_ok=True)

    for i, item in enumerate(train_item_list):
      object_path = train_item_list.x.items[i]

      if item[1].obj == "back-squat":
        shutil.copy(object_path, PROCESSED_DATA_TRAIN_DIRNAME / 'back-squat')

      elif item[1].obj == "front-squat":
        shutil.copy(object_path, PROCESSED_DATA_TRAIN_DIRNAME / 'front-squat')

    for i, item in enumerate(valid_item_list):
      object_path = valid_item_list.x.items[i]

      if item[1].obj == "back-squat":
        shutil.copy(object_path, PROCESSED_DATA_VALID_DIRNAME / 'back-squat')

      elif item[1].obj == "front-squat":
        shutil.copy(object_path, PROCESSED_DATA_VALID_DIRNAME / 'front-squat')
        
    data = (src.transform(get_transforms(), size=self.image_size)
            .databunch().normalize(imagenet_stats))

    ## data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
    ##        ds_tfms=get_transforms(), size=self.image_size, num_workers=4).normalize(imagenet_stats)
    return data

  def _save_processed_fvbs_dataset(self, data: ImageDataBunch) -> None:
    """Saves ImageDataBunch in a .h5 file for later use."""

    # TODO: Fix serializaion.
    print("Saving ImageDataBunch to HDF5 in a compressed format...")
    PROCESSED_DATA_DIRNAME.mkdir(parents=True, exist_ok=True)

    train_ds = data.train_ds
    val_ds = data.valid_ds


    with h5py.File(PROCESSED_DATA_FILENAME, "w") as f:
      f.create_dataset("train_ds", data=train_ds, dtype="u1", compression="lzf")
      f.create_dataset("val_ds", data=train_ds, dtype="u1", compression="lzf")

  def _save_essential_dataset_params(self, data: ImageDataBunch) -> None:
    """
    Save essential dataset parameters in a .json file at a canonical location 
    (See `ESSENTIAL_FILENAME` above).
    """
    print("Saving essential dataset parameters to squat_recognizer/datasets...")

    essentials = {"classes": data.classes, "input_shape": list(data.train_ds[0][0].shape)}

    with open(ESSENTIAL_FILENAME, "w") as f:
      json.dump(essentials, f)

  def _clean_up(self):
    print("Cleaning up...")
    root_dir = os.getcwd()
    os.chdir(RAW_DATA_DIRNAME)
    shutil.rmtree("fvbs_dataset")
    os.chdir(root_dir)

  def __repr__(self):
    return self.data.__repr__