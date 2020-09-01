"""Tests for FvbsDataset class."""

from shutil import rmtree
import os
import unittest
import pytest

from squat_recognizer.datasets.fvbs_dataset import FvbsDataset
from squat_recognizer.datasets.dataset import Dataset

RAW_DATA_DIRNAME = Dataset.data_dirname() / "raw" / "fvbs"
PROCESSED_DATA_DIRNAME = Dataset.data_dirname() / "processed" / "fvbs"
PROCESSED_DATA_VALID_DIRNAME = PROCESSED_DATA_DIRNAME / "valid"
PROCESSED_DATA_TRAIN_DIRNAME = PROCESSED_DATA_DIRNAME / "train"
ESSENTIAL_FILENAME = FvbsDataset.essential_dirname()


class TestFvbsDataset(unittest.TestCase):
    """Tests for FvbsDataset class."""

    def setUp(self):
        self.dataset = FvbsDataset()

    def test_create_fvbs_dataset(self):
        fvbs_dataset = FvbsDataset()

    def test_load_or_generate_data(self):
        self.dataset.load_or_generate_data()
        self.assertTrue(os.path.exists(RAW_DATA_DIRNAME))
        self.assertTrue(os.path.exists(PROCESSED_DATA_DIRNAME))
        self.assertTrue(os.path.exists(PROCESSED_DATA_TRAIN_DIRNAME))
        self.assertTrue(os.path.exists(PROCESSED_DATA_VALID_DIRNAME))

    @pytest.mark.skip(reason="unstable test. Removed files before acting.")
    def test_load_or_generate_data_by_removing_data_first(self):
        zip_name = "front_vs_back_dataset.zip"
        if os.path.exists(RAW_DATA_DIRNAME / zip_name):
            os.remove(RAW_DATA_DIRNAME / zip_name)

        if os.path.exists(PROCESSED_DATA_DIRNAME):
            rmtree(PROCESSED_DATA_DIRNAME)

        if os.path.exists(ESSENTIAL_FILENAME):
            os.remove(ESSENTIAL_FILENAME)

        self.dataset.load_or_generate_data()
        self.assertTrue(os.path.exists(RAW_DATA_DIRNAME))
        self.assertTrue(os.path.exists(PROCESSED_DATA_DIRNAME))
        self.assertTrue(os.path.exists(PROCESSED_DATA_TRAIN_DIRNAME))
        self.assertTrue(os.path.exists(PROCESSED_DATA_VALID_DIRNAME))
