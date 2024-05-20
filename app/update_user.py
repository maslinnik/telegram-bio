from app import app, db, api_manager
from app.models import Username, Update
import sqlalchemy as sa
from typing import Iterable

app.app_context().push()


def update_users(users: Iterable[Username]):
    bio_list = api_manager.get_bio_batch([user.username for user in users])
    for user, current_bio in zip(users, bio_list):
        last_bio_obj = db.session.scalar(sa.select(Update)
                                         .where(Update.user == user)
                                         .order_by(sa.desc(Update.timestamp)))
        if not last_bio_obj or last_bio_obj.body != current_bio:
            db.session.add(Update(body=current_bio, user=user))
            db.session.commit()


def update_user(user: Username):
    update_users([user])
