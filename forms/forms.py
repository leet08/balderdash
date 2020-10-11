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
    response1 = StringField('Your ending:')
    response2 = StringField('Your ending:')
    response3 = StringField('Your ending:')
    response4 = StringField('Your ending:')
    response5 = StringField('Your ending:')
    submit = SubmitField('Submit')

class VoteForm(FlaskForm):
    #voting1 = RadioField('Question 1 Vote', choices = [('val','desc')])
    #voting2 = RadioField('Question 2 Vote', choices = [])
    #voting3 = RadioField('Question 3 Vote', choices = [])
    submit = SubmitField('Submit')

class RemoveUserForm(FlaskForm):
    submit = SubmitField('Submit')

class NewpostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
