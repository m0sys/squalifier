"""Integration testing for prediction REST api."""
import os
from pathlib import Path
import unittest

from fastapi import Response
from fastapi.testclient import TestClient

from api.app import app

os.environ["CUDA_VISIBLE_DEVICES"] = ""

REPO_DIRNAME = Path(__file__).parents[2].resolve()
SUPPORT_DIRNAME = REPO_DIRNAME / "squat_recognizer" / "tests" / "support"


class TestIntegrations(unittest.TestCase):
    """Integration tests for prediction REST api."""

    def setUp(self):
        self.client = TestClient(app)

    def test_index(self):
        res: Response = self.client.get("/")
        assert res.status_code == 200
        assert res.json() == {"msg": "Hello World!"}

    def test_predict_route_existance(self):
        files = {"file": open(SUPPORT_DIRNAME / "back2.jpg", "rb")}
        res: Response = self.client.post("/v1/predict", files=files)
        assert res.status_code == 200

    def test_predict_route_on_image(self):
        files = {"file": open(SUPPORT_DIRNAME / "back2.jpg", "rb")}
        res: Response = self.client.post("/v1/predict", files=files)
        assert res.status_code == 200
        assert res.json() == {"pred": "back-squat"}

    def test_predict_route_on_two_images(self):
        files = {"file": open(SUPPORT_DIRNAME / "back2.jpg", "rb")}
        res: Response = self.client.post("/v1/predict", files=files)
        assert res.status_code == 200
        assert res.json() == {"pred": "back-squat"}

        files = {"file": open(SUPPORT_DIRNAME / "front2.jpg", "rb")}
        res: Response = self.client.post("/v1/predict", files=files)
        assert res.status_code == 200
        assert res.json() == {"pred": "front-squat"}
