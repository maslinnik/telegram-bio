from test_model import TestCaseModel
from app.models import User, Username, Update
from app import db, app
from unittest.mock import patch, Mock


class TestForms(TestCaseModel):
    @patch('app.forms.UserExists.__call__')
    def test_add_user(self, _):
        with self.client:
            self._send_auth_request()
            self.client.post("/updates/add_user", data={"username": "username"})
            self.client.post("/updates/add_user", data={"username": "another_username"})

            users = db.session.query(Username).order_by(Username.username).all()
            self.assertEqual(len(users), 2)
            self.assertEqual(users[0].username, "another_username")
            self.assertEqual(users[0].monitored, True)
            self.assertEqual(users[1].username, "username")
            self.assertEqual(users[1].monitored, True)

    @patch('app.forms.UserExists.__call__')
    def test_remove_user(self, _):
        with self.client:
            self._send_auth_request()
            self.client.post("/updates/add_user", data={"username": "username"})
            self.client.post("/updates/add_user", data={"username": "another_username"})
            id_to_delete = db.session.query(Username).where(Username.username == "username").first().id
            self.client.post("/updates/remove_user", data={"id": id_to_delete})

            users = db.session.query(Username).order_by(Username.username).all()
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].username, "another_username")

    @patch('app.forms.UserExists.__call__')
    def test_toggle_monitor(self, _):
        with self.client:
            self._send_auth_request()
            self.client.post("/updates/add_user", data={"username": "username"})
            id = db.session.query(Username).where(Username.username == "username").first().id
            self.client.post("/updates/unmonitor_user", data={"id": id})
            self.assertEqual(db.session.query(Username).first().monitored, False)
            self.client.post("/updates/unmonitor_user", data={"id": id})
            self.assertEqual(db.session.query(Username).first().monitored, False)
            self.client.post("/updates/monitor_user", data={"id": id})
            self.assertEqual(db.session.query(Username).first().monitored, True)
            self.client.post("/updates/monitor_user", data={"id": id})
            self.assertEqual(db.session.query(Username).first().monitored, True)

    @patch('app.forms.UserExists.__call__')
    @patch('app.api_manager.WebScraper.get_bio')
    def test_force_update(self, get_bio_call: Mock, _):
        with self.client:
            self._send_auth_request()
            user = Username(username="username", monitored=True)
            db.session.add(user)
            db.session.commit()
            get_bio_call.side_effect = ["bio_sample", "another_bio_sample"]
            self.client.post("/updates/username/force")
            self.client.post("/updates/username/force")
            get_bio_call.assert_called_with("username")
            self.assertEqual(get_bio_call.call_count, 2)

            updates = db.session.query(Update).where(Update.user == user).order_by(Update.timestamp).all()
            self.assertEqual(len(updates), 2)
            self.assertEqual(list(map(lambda u: u.body, updates)), ["bio_sample", "another_bio_sample"])

    @patch('app.forms.UserExists.__call__')
    @patch('app.api_manager.WebScraper.get_bio')
    def test_delete_update(self, get_bio_call: Mock, _):
        with (self.client):
            self._send_auth_request()
            user = Username(username="username", monitored=True)
            db.session.add(user)
            db.session.commit()
            get_bio_call.side_effect = ["first_bio", "second_bio", "first_bio"]
            self.client.post("/updates/username/force")
            self.client.post("/updates/username/force")
            self.client.post("/updates/username/force")
            update_1, update_2, update_3 = (db.session
                                            .query(Update)
                                            .where(Update.user == user)
                                            .order_by(Update.timestamp)
                                            .all())
            self.client.post("updates/username/remove", data={"id": update_2.id})
            new_updates = db.session.query(Update).where(Update.user == user).order_by(Update.timestamp).all()
            self.assertEqual(new_updates, [update_1])