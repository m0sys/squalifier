"""Integration testing for prediction GraphQL api."""
import os
from pathlib import Path
import pytest
import unittest
from fastapi import Response
from fastapi.testclient import TestClient

from api.graphql_app import app

os.environ["CUDA_VISIBLE_DEVICES"] = ""

REPO_DIRNAME = Path(__file__).parents[2].resolve()
SUPPORT_DIRNAME = REPO_DIRNAME / "squat_recognizer" / "tests" / "support"


class TestIntegrations(unittest.TestCase):
    """Integration tests for prediction GraphQL api."""

    def setUp(self):
        self.client = TestClient(app)

    def test_index(self):
        res: Response = self.client.get("/")
        assert res.status_code == 200
        assert res.json() == {"msg": "Hello World!"}

    def test_info_query(self):
        query = """
        query {
          info
        }
        """

        res: Response = self.client.post("/graphql", json={"query": query})

        assert res.status_code == 200
        assert res.json()["data"] is not None
