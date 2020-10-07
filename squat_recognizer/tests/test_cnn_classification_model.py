"""Tests for CnnClassificationModel class."""
import os
from pathlib import Path
import unittest
import pytest

from fastai.vision import open_image

from squat_recognizer.models import CnnClassificationModel
from squat_recognizer.tests._test_utils import get_label

SUPPORT_DIRNAME = Path(__file__).parents[0].resolve() / "support"
os.environ["CUDA_VISIBLE_DEVICES"] = ""


class TestCnnClassificationModel(unittest.TestCase):
    """Tests for CnnClassificationModel class."""

    def setUp(self):
        self.model = CnnClassificationModel()
        self.support_dir = Path("./squat_recognizer/tests/support")
        img1 = open_image(SUPPORT_DIRNAME / "back2.jpg")
        img2 = open_image(SUPPORT_DIRNAME / "front2.jpg")
        img3 = open_image(SUPPORT_DIRNAME / "back1.jpg")
        img4 = open_image(SUPPORT_DIRNAME / "front1.jpg")
        self.images = [img1, img2, img3, img4]

    def test_create_cnn_classification_model(self):
        model = CnnClassificationModel()

    ## @pytest.mark.skip(reason="test if you have time to kill")
    def test_fit(self):
        stage_one = {"epochs": 1, "one_cycle": 1}

        self.model.fit(stage_one)

    @pytest.mark.skip(reason="test if you have time to kill")
    def test_fit_with_two_stages(self):
        stage_one = {"epochs": 1, "one_cycle": 1}
        stage_two = {"unfreeze": 1, "epochs": 1, "one_cycle": 1, "max_lr_start": 3e-5, "max_lr_end": 3e-4}

        self.model.fit(stage_one, stage_two)

    @pytest.mark.skip(reason="test if you have already trained state-1 model.")
    def test_load_weights_stage_one(self):
        self.model.load_weights("stage-1")

    @pytest.mark.skip(reason="test if you have already trained stage-2 model.")
    def test_load_weight_stage_two(self):
        self.model.load_weights("stage-2")

    @pytest.mark.skip(reason="test if you have already trained state-1 model.")
    def test_load_weights_stage_one_then_predict(self):
        self.model.load_weights("stage-1")
        pred, _ = self.model.predict(self.images[0])
        self.assertEqual(pred, "back-squat")

    @pytest.mark.skip(reason="test if you have already trained state-1 model.")
    def test_load_weight_stage_one_then_predict_all_images(self):
        self.model.load_weights("stage-1")
        for i, image in enumerate(self.images):
            label = get_label(i)
            pred, _ = self.model.predict(image)
            self.assertEqual(pred, label, f"failed to predict label {label} on image at idx {i}")

    @pytest.mark.skip(reason="test if you have already trained stage-2 model.")
    def test_load_weight_stage_two_then_predict_all_images(self):
        self.model.load_weights("stage-2")
        for i, image in enumerate(self.images):
            label = get_label(i)
            pred, _ = self.model.predict(image)
            self.assertEqual(pred, label, f"failed to predict label {label} on image at idx {i}")

    def test_load_export_then_predict(self):
        self.model.load_export()
        pred, _ = self.model.predict(self.images[0])
        self.assertEqual(pred, "back-squat")

    def test_load_export_then_predict_all_images(self):
        self.model.load_export()
        for i, image in enumerate(self.images):
            label = get_label(i)
            pred, _ = self.model.predict(image)
            self.assertEqual(pred, label, f"failed to predict label {label} on image at idx {i}")
