from flask_login import login_user
from test_model import TestCaseModel
from app.models import User, Username
from app import db, app
from unittest.mock import patch, MagicMock


class TestAuth(TestCaseModel):
    def __send_auth_request(self):
        user = User(username="admin")
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()
        self.client.post("/auth/login", data={
            "username": "admin",
            "password": "admin",
        })

    def test_profile_unauthorized(self):
        response = self.client.get("/profile")
        self.assertEqual(response.status_code, 401)

    def test_profile_authorized(self):
        with self.client:
            self.__send_auth_request()
            response = self.client.get("/profile")
            self.assertEqual(response.status_code, 200)

    def test_updates_edit_user_unauthorized(self):
        response = self.client.post("/updates/add_user", data={"username": "username"})
        self.assertEqual(response.status_code, 401)
        response = self.client.post("/updates/remove_user", data={"id": 12})
        self.assertEqual(response.status_code, 401)

    @patch('app.forms.UserExists.__call__')
    def test_updates_edit_user_authorized(self, _):
        with self.client:
            self.__send_auth_request()
            response = self.client.post("/updates/add_user", data={"username": "username"})
            self.assertEqual(response.status_code, 302)
            response = self.client.post("/updates/remove_user", data={"id": 12})
            self.assertEqual(response.status_code, 302)

    def test_updates_toggle_monitor_user_unauthorized(self):
        response = self.client.post("/updates/monitor_user", data={"id": 12})
        self.assertEqual(response.status_code, 401)
        response = self.client.post("/updates/unmonitor_user", data={"id": 12})
        self.assertEqual(response.status_code, 401)

    def test_updates_toggle_monitor_user_authorized(self):
        with self.client:
            self.__send_auth_request()
            response = self.client.post("/updates/monitor_user", data={"id": 12})
            self.assertEqual(response.status_code, 302)
            response = self.client.post("/updates/unmonitor_user", data={"id": 12})
            self.assertEqual(response.status_code, 302)

    def test_updates_edit_updates_unauthorized(self):
        with self.client:
            user = Username(username="username", monitored=True)
            db.session.add(user)
            db.session.commit()
            self.assertEqual(self.client.get("/updates/username").status_code, 200)
            response = self.client.post("/updates/username/force", data={"id": 12})
            self.assertEqual(response.status_code, 401)
            response = self.client.post("/updates/username/remove", data={"id": 13})
            self.assertEqual(response.status_code, 401)

    def test_updates_edit_updates_authorized(self):
        with self.client:
            self.__send_auth_request()
            user = Username(username="username", monitored=True)
            db.session.add(user)
            db.session.commit()
            self.assertEqual(self.client.get("/updates/username").status_code, 200)
            response = self.client.post("/updates/username/force", data={"id": 12})
            self.assertEqual(response.status_code, 302)
            response = self.client.post("/updates/username/remove", data={"id": 13})
            self.assertEqual(response.status_code, 302)