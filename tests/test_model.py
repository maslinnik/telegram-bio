import unittest
from app import app, db
from app.models import User


class TestCaseModel(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _send_auth_request(self):
        user = User(username="admin")
        user.set_password("admin")
        db.session.add(user)
        db.session.commit()
        self.client.post("/auth/login", data={
            "username": "admin",
            "password": "admin",
        })
