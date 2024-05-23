from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
from flask_login import UserMixin


class Username(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    monitored: so.Mapped[bool] = so.mapped_column(sa.Boolean)

    updates: so.WriteOnlyMapped['Update'] = so.relationship(back_populates='user', passive_deletes=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Update(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True,
                                                      default=lambda: datetime.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Username.id),
                                               index=True)

    user: so.Mapped[Username] = so.relationship(back_populates='updates')

    def __repr__(self):
        return "<Update '{}'>".format(self.body)


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
