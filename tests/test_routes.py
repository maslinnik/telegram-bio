import os
import unittest
from app import app, db
from test_model import TestCaseModel


class TestRoutes(TestCaseModel):
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
