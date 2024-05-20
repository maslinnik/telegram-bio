from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, StopValidation
from wtforms.widgets import HiddenInput
from app import api_manager


class UserExists():
    def __init__(self):
        pass

    def __call__(self, form, field):
        if api_manager.user_exists(field.data):
            return

        raise StopValidation('This user does not exist.')


class AddUserForm(FlaskForm):
    username = StringField('Username (w/o @)', validators=[DataRequired(), UserExists()])
    submit = SubmitField('Add')


class RemoveUserForm(FlaskForm):
    id = IntegerField()
    submit = SubmitField('Remove')


class StartMonitoringUserForm(FlaskForm):
    id = IntegerField()
    submit = SubmitField('Start monitoring')


class StopMonitoringUserForm(FlaskForm):
    id = IntegerField()
    submit = SubmitField('Stop monitoring')


class ForceUpdateForm(FlaskForm):
    submit = SubmitField('Force update')


class RemoveUpdateForm(FlaskForm):
    id = IntegerField()
    submit = SubmitField('Remove')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
