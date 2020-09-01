"""Tests for SquatRecognizer class."""
import os
from pathlib import Path
import unittest

from random import choice as random_choice
from fastai.vision import open_image

from squat_recognizer.squat_recognizer import SquatRecognizer

SUPPORT_DIRNAME = Path(__file__).parents[0].resolve() / "support"

os.environ["CUDA_VISIBLE_DEVICES"] = ""


class TestSquatRecognizer(unittest.TestCase):
    """Tests for SquatRecognizer class."""

    def setUp(self):
        self.recognizer = SquatRecognizer()
        self.support_dir = Path("./squat_recognizer/tests/support")
        img1 = open_image(self.support_dir / "back2.jpg")
        img2 = open_image(self.support_dir / "front2.jpg")
        img3 = open_image(self.support_dir / "back1.jpg")
        img4 = open_image(self.support_dir / "front1.jpg")
        self.images = [img1, img2, img3, img4]
        self.threshold = 0.9

    def test_create_squat_recognizer(self):
        """Test to see whether SquatRecognizer can be instantiated"""
        recognizer = SquatRecognizer()

    def test_predict_exists(self):
        self.recognizer.predict()

    def test_predict_on_one_image(self):
        img = self.images[0]
        self.recognizer.predict(img)

    def test_prediction_on_one_image(self):
        img = self.images[0]
        pred, _ = self.recognizer.predict(img)
        self.assertEqual(pred, "back-squat", "failed to predict label 'back-squat' on image 'back2.jpg'")

    def test_prediction_on_two_images(self):
        pred1, _ = self.recognizer.predict(self.images[0])
        pred2, _ = self.recognizer.predict(self.images[1])

        self.assertEqual(pred1, "back-squat", "failed to predict label 'back-squat' on image 'back2.jpg'")
        self.assertEqual(pred2, "front-squat", "failed to predict label 'front-squat' on image 'front2.jpg'")

    def test_prediction_on_three_random_images(self):
        indicies = [0, 1, 2, 3]
        idx1 = random_choice(indicies)
        idx2 = random_choice(indicies)
        idx3 = random_choice(indicies)

        pred1, _ = self.recognizer.predict(self.images[idx1])
        pred2, _ = self.recognizer.predict(self.images[idx2])
        pred3, _ = self.recognizer.predict(self.images[idx3])

        self.assertEqual(pred1, _get_label(idx1), f"failed to predict label {_get_label(idx1)} on image at idx {idx1}")
        self.assertEqual(pred2, _get_label(idx2), f"failed to predict label {_get_label(idx2)} on image at idx {idx2}")
        self.assertEqual(pred3, _get_label(idx3), f"failed to predict label {_get_label(idx3)} on image at idx {idx3}")

    def test_prediction_confidence_on_one_image(self):
        pred, conf = self.recognizer.predict(self.images[0])
        self.assertEqual(pred, "back-squat", "failed to predict label 'back-squat' on image 'back2.jpg'")
        self.assertGreaterEqual(
            conf, self.threshold, f"failed test... conf of {conf} is not greater than {self.threshold}"
        )

    def test_all_image_conf_greater_than_threshold(self):
        for i, img in enumerate(self.images):
            pred, conf = self.recognizer.predict(img)
            self.assertEqual(pred, _get_label(i), f"failed to predict label {_get_label(i)} on image at idx {i}")
            self.assertGreaterEqual(
                conf, self.threshold, f"failed test... conf of {conf} is not greater than {self.threshold}"
            )


def _get_label(idx) -> str:
    if idx % 2 == 0:
        return "back-squat"
    else:
        return "front-squat"


if __name__ == "__main__":
    unittest.main()
