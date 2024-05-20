from app import app, db
from app.models import User
import os

app.app_context().push()

db.create_all()

ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

db.session.query(User).delete()
user = User(username=ADMIN_LOGIN)
user.set_password(ADMIN_PASSWORD)
db.session.add(user)
db.session.commit()
