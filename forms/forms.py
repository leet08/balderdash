from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class CreateGame(FlaskForm):
	createFirstPlayer = StringField('Username', validators=[DataRequired()])
	createRounds = StringField('Number of Rounds', validators=[DataRequired()])
	createPlayers = StringField('Number of Players', validators=[DataRequired()])
	submit = SubmitField('Create new game')

class EnterGame(FlaskForm):
	gameID = StringField('Enter Game ID', validators=[DataRequired()])
	username = StringField('Create a Username', validators=[DataRequired()])
	submit = SubmitField('Enter game')

class PlayForm(FlaskForm):
    response = StringField('Your ending:')
    submit = SubmitField('Submit')

class VoteForm(FlaskForm):
    voting = StringField('Your choice:')
    submit = SubmitField('Submit')

class RemoveUserForm(FlaskForm):
    submit = SubmitField('Submit')

