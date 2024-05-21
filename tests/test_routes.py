from flask_login import login_user
from test_model import TestCaseModel
from app.models import User
from app import db, app


class TestRoutes(TestCaseModel):
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
