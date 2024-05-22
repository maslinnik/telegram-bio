from app import app, db, api_manager
from flask import render_template, redirect, url_for, flash, request
import sqlalchemy as sa
from app.models import Username, Update, User
from app.forms import *
from app.update_user import update_user
from flask_login import current_user, login_user, login_required, logout_user, fresh_login_required


@app.route('/')
def index():
    return render_template('index.html', title='Telegram Bio Updates')


@app.route('/updates')
def updates_hub():
    monitored_users = (db.session.query(Username)
                       .filter(Username.monitored == True)
                       .order_by(Username.username)
                       .all())
    unmonitored_users = (db.session.query(Username)
                         .filter(Username.monitored == False)
                         .order_by(Username.username)
                         .all())
    monitored_data = []
    for user in monitored_users:
        updates = db.session.query(Update).where(Update.user == user).order_by(Update.timestamp).all()
        monitored_data.append((user, updates, StopMonitoringUserForm(), RemoveUserForm()))
    unmonitored_data = []
    for user in unmonitored_users:
        updates = db.session.query(Update).where(Update.user == user).order_by(Update.timestamp).all()
        unmonitored_data.append((user, updates, StartMonitoringUserForm(), RemoveUserForm()))
    form = AddUserForm()
    return render_template('updates_hub.html',
                           title='Updates',
                           monitored_data=monitored_data,
                           unmonitored_data=unmonitored_data,
                           show_admin=current_user.is_authenticated,
                           form=form)


@app.route('/updates/add_user', methods=['POST'])
@fresh_login_required
def updates_add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = db.session.query(Username).where(Username.username == form.username.data).first()
        if user is None:# and api_manager.user_exists(form.username.data):
            db.session.add(Username(username=form.username.data, monitored=True))
            db.session.commit()
    return redirect(url_for('updates_hub'))


@app.route('/updates/remove_user', methods=['POST'])
@fresh_login_required
def updates_remove_user():
    form = RemoveUserForm()
    if form.validate_on_submit():
        user = db.session.query(Username).where(Username.id == form.id.data).first()
        if user is not None:
            user_updates = db.session.query(Update).where(Update.user == user).all()
            for u in user_updates:
                db.session.delete(u)
            db.session.delete(user)
            db.session.commit()
    return redirect(url_for('updates_hub'))


@app.route('/updates/monitor_user', methods=['POST'])
@fresh_login_required
def updates_monitor_user():
    form = StartMonitoringUserForm()
    if form.validate_on_submit():
        user = db.session.query(Username).where(Username.id == form.id.data).first()
        if user is not None:
            user.monitored = True
            db.session.commit()
    return redirect(url_for('updates_hub'))


@app.route('/updates/unmonitor_user', methods=['POST'])
@fresh_login_required
def updates_unmonitor_user():
    form = StopMonitoringUserForm()
    if form.validate_on_submit():
        user = db.session.query(Username).where(Username.id == form.id.data).first()
        if user is not None:
            user.monitored = False
            db.session.commit()
    return redirect(url_for('updates_hub'))


@app.route('/updates/<username>')
def updates_list(username):
    user = db.first_or_404(sa.select(Username).where(Username.username == username))
    updates = db.session.query(Update).where(Update.user == user).order_by(Update.timestamp).all()
    updates_data = [(update, RemoveUpdateForm()) for update in updates]
    force_update_form = ForceUpdateForm()
    return render_template('updates_list.html',
                           user=user,
                           updates_data=updates_data,
                           force_update_form=force_update_form,
                           show_admin=current_user.is_authenticated,
                           title=f"{user.username}'s Updates")


@app.route('/updates/<username>/force', methods=['POST'])
@fresh_login_required
def force_update(username):
    form = ForceUpdateForm()
    if form.validate_on_submit():
        user = db.first_or_404(sa.select(Username).where(Username.username == username))
        update_user(user)
    return redirect(url_for('updates_list', username=username))


@app.route('/updates/<username>/remove', methods=['POST'])
@fresh_login_required
def updates_remove(username):
    form = RemoveUpdateForm()
    if form.validate_on_submit():
        user = db.first_or_404(sa.select(Username).where(Username.username == username))
        update = db.session.query(Update).where(Update.id == form.id.data).first()
        if update is not None:
            next_update = (db.session.query(Update)
                           .where(Update.user == update.user)
                           .order_by(Update.timestamp)
                           .filter(Update.timestamp > update.timestamp)
                           .first())
            prev_update = (db.session.query(Update)
                           .where(Update.user == update.user)
                           .order_by(Update.timestamp.desc())
                           .filter(Update.timestamp < update.timestamp)
                           .first())
            if update.user == user:
                db.session.delete(update)
                if next_update is not None and prev_update is not None and prev_update.body == next_update.body:
                    db.session.delete(next_update)
                db.session.commit()
    return redirect(url_for('updates_list', username=username))


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In')


@app.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@fresh_login_required
def profile():
    return render_template('profile.html', username=current_user.username, title='My Profile')
