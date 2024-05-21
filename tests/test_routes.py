from flask_login import login_user
from test_model import TestCaseModel
from app.models import User, Username
from app import db, app
from mock import patch, Mock


class TestRoutes(TestCaseModel):
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    @patch('app.forms.UserExists.__call__')
    def test_updates_hub_unauthorized(self, _):
        with self.client:
            self._send_auth_request()
            self.client.post("/updates/add_user", data={"username": "username"})
            id = db.session.query(Username).where(Username.username == "username").first().id
            self.client.post("/updates/unmonitor_user", data={"id": id})
            self.client.post("/updates/add_user", data={"username": "new_username"})
            self.client.get("/auth/logout")
            response = self.client.get("/updates")
            self.assertEqual(response.status_code, 200)

    @patch('app.forms.UserExists.__call__')
    def test_updates_hub_authorized(self, _):
        with self.client:
            self._send_auth_request()
            self.client.post("/updates/add_user", data={"username": "username"})
            id = db.session.query(Username).where(Username.username == "username").first().id
            self.client.post("/updates/unmonitor_user", data={"id": id})
            self.client.post("/updates/add_user", data={"username": "new_username"})
            response = self.client.get("/updates")
            self.assertEqual(response.status_code, 200)
