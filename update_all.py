import time

from app import app, db
from app.models import Username
from app.update_user import update_users
import signal
from threading import Event

exit = Event()


def main():
    while not exit.is_set():
        print('Starting to update')
        try:
            with app.app_context():
                users = db.session.query(Username).filter(Username.monitored == True).all()
                update_users(users)
        except Exception as e:
            print('Following exception occurred:')
            print(e)
        else:
            print(f'Updated {len(users)} users')
        exit.wait(60)


def quit(*_):
    print("Request to shutdown received, stopping")
    exit.set()


signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

main()
