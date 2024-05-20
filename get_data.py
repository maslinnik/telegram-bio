from time import sleep
from app import app, db
from app.models import Username, Update, User
import sqlalchemy as sa
from update_user import update_users

app.app_context().push()

while True:
    users = db.session.query(Username).filter(Username.monitored == True).all()
    update_users(users)
    sleep(60)
