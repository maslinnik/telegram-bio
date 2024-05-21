import os
import unittest
from app import app, db


class UserModelCase(unittest.TestCase):
    def setUp(self):
        os.environ['DATABASE_URL'] = 'sqlite://'
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
