"""Utility functions for squat_recognizer module."""
from pathlib import Path
from typing import Union
from urllib.request import urlopen, urlretrieve, Request
import hashlib
import os

import numpy as np
import cv2
from tqdm import tqdm
import boto3


def read_image(image_uri: Union[Path, str], grayscale=False) -> np.array:
    """Read image_uri."""

    def read_image_from_filename(image_filename, imread_flag):
        return cv2.imread(str(image_filename), imread_flag)

    def read_image_from_url(image_url, imread_flag):
        if image_url.lower().startswith("https"):
            req = Request(image_url)  # nosec
            with urlopen(req) as res:  # nosec
                img_array = np.array(bytearray(res.read()), dtype=np.uint8)
                return cv2.imdecode(img_array, imread_flag)
        else:
            raise ValueError from None

    imread_flag = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
    local_file = os.path.exists(image_uri)

    try:
        img = None
        if local_file:
            img = read_image_from_filename(image_uri, imread_flag)

        else:
            img = read_image_from_url(image_uri, imread_flag)

        assert img is not None

    except Exception as e:
        raise ValueError("Cloud not load image at {}: {}".format(image_uri, e))

    return img


def write_image(image: np.ndarray, filename: Union[Path, str]) -> None:
    """Write image to file."""
    cv2.imwrite(str(filename), image)


def compute_sha256(filename: Union[Path, str]):
    """Return SHA256 checksum of a file"""
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class TqdmUpTo(tqdm):
    """From https://github.com/tqdm/tqdm/blob/master/examples/tqdm_wget.py"""

    def update_to(self, blocks=1, bsize=1, tsize=None):
        """
    Parameters
    ----------
    blocks : int, optional
        Number of blocks transferred so far [default: 1].
    bsize  : int, optional
        Size of each block (in tqdm units) [default: 1].
    tsize  : int, optional
        Total size (in tqdm units). If [default: None] remains unchanged.
    """
        if tsize is not None:
            self.total = tsize  # pylint: disable=attribute-defined-outside-init
        self.update(blocks * bsize - self.n)  # will also set self.n = b * bsize


def download_url(url, filename):
    """Download a file from url to filename, with progress bar."""
    with TqdmUpTo(unit="B", unit_scale=True, unit_divisor=1024, miniters=1) as t:
        urlretrieve(url, filename, reporthook=t.update_to, data=None)  # nosec


def _hook(t):
    def inner(bytes_amount):
        t.update(bytes_amount)

    return inner


def download_object_from_s3(bucket, obj, filename):
    """Download a file from s3 to filename, with progress bar."""
    aws_s3 = boto3.client("s3")
    with TqdmUpTo(unit="B", unit_scale=True, unit_divisor=1024, miniters=1) as t:
        aws_s3.download_file(bucket, obj, filename, Callback=_hook(t))
