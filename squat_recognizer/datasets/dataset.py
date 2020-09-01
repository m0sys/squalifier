"""Dataset class to be extended by dataset-specific classes."""
from pathlib import Path
import argparse
from argparse import Namespace
import os
import zipfile

from squat_recognizer import utils


class Dataset:
    """Simple abstract calss for datasets."""

    def __init__(self, **kwargs):
        pass

    @classmethod
    def data_dirname(cls) -> Path:
        return Path(__file__).resolve().parents[2] / "data"

    def load_or_generate_data(self):
        raise NotImplementedError


def _download_raw_dataset(metadata) -> None:
    if os.path.exists(metadata["filename"]):
        return
    print(f"Downloading raw dataset from {metadata['url']}...")
    utils.download_url(metadata["url"], metadata["filename"])
    print("Computing SHA-256...")
    sha256 = utils.compute_sha256(metadata["filename"])
    if sha256 != metadata["sha256"]:
        raise ValueError("Downloaded data file SHA-256 does not match that listed in metadata document.")


def _download_raw_dataset_from_s3(metadata) -> None:
    if os.path.exists(metadata["filename"]):
        return
    print(f"Downloading raw dataset from {metadata['bucket']}/{metadata['object']}...")
    utils.download_object_from_s3(metadata["bucket"], metadata["object"], metadata["filename"])
    print("Computing SHA-256...")
    sha256 = utils.compute_sha256(metadata["filename"])
    if sha256 != metadata["sha256"]:
        raise ValueError("Downloaded data file SHA-256 does not match that listed in metadata document.")


def _extract_raw_dataset(metadata, location) -> None:
    print(f"Extracting {metadata['filename']}...")
    with zipfile.ZipFile(metadata["filename"], "r") as zip_file:
        zip_file.extractall(location)


def _parse_args() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subsample_fraction", type=float, default=None, help="If given, is used as the fraction of data to expose.",
    )
    return parser.parse_args()
