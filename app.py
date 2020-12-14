from dotenv import load_dotenv
from flask import Flask, flash, render_template, request, url_for, redirect, jsonify, session
from models.models import Db, Game, User, Question
from forms.forms import CreateGame, EnterGame, PlayForm, VoteForm, RemoveUserForm
from os import environ
import sys
from passlib.hash import sha256_crypt
from sqlalchemy import func, and_, or_, not_
import random
import numpy as np
from flask_heroku import Heroku

load_dotenv('.env')

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/balderdash'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
app.secret_key = environ.get('SECRET_KEY')
Db.init_app(app)

# the empty default profile, also test1 first added to current game is user 1
testProfile = '152'
emptyProfile = '153'
adminProfile = '154'
blankQuestion = '1'
randomSeed = 0


#GET /
@app.route('/')
@app.route('/enter', methods=['GET', 'POST'])
def enter():

    form = EnterGame()

    if request.method == 'POST':
        # Init credentials from form request
        gameID = request.form['gameID']
        username = request.form['username']
        session['username'] = username	    
        session['gameID'] = gameID

        # show players to player1 waiting room?
        currentGame = Game.query.filter_by(gid=gameID).first()

        # user = User(username = username, response1 = 'blank', response2 = 'blank', response3 = 'blank', voting1 = 0, voting2 = 0, voting3 = 0) # create new user with blanks
        # Db.session.add(user)
        # Db.session.commit()

        # check if they are already in the game and can reenter. current player list
        player1 = User.query.filter_by(uid=currentGame.player1).first()
        player2 = User.query.filter_by(uid=currentGame.player2).first()
        player3 = User.query.filter_by(uid=currentGame.player3).first()
        player4 = User.query.filter_by(uid=currentGame.player4).first()
        player5 = User.query.filter_by(uid=currentGame.player5).first()
        players = [player1, player2, player3, player4, player5] 

        userFlag = False
        for p in players: 

            if p.username == username:
                userFlag = True
                if p == player1:
                    session['uid'] = player1.uid
                if p == player2:
                    session['uid'] = player2.uid
                if p == player3:
                    session['uid'] = player3.uid
                if p == player4:
                    session['uid'] = player4.uid
                if p == player5:
                    session['uid'] = player5.uid

        if userFlag == False and username != 'ADMIN':
            # create a new user
            user = User(username = username, response1 = 'blank', response2 = 'blank', response3 = 'blank', response4= 'blank',response5 = 'blank',voting1 = 0, voting2 = 0, voting3 = 0, voting4 = 0, voting5 = 0) # create new user with blanks
            Db.session.add(user)
            Db.session.commit()

            # add to the game backwards from empties (user 46)
            currentPlayers = [currentGame.player1, currentGame.player2, currentGame.player3, currentGame.player4, currentGame.player5]
            for p in currentPlayers:
                if p == emptyProfile or p == testProfile:
                    if p == currentGame.player1: 
                        user.playernumber = 1
                        currentGame.player1 = user.uid
                        Db.session.add(user)
                        Db.session.add(currentGame)
                        break
                    if p == currentGame.player2: 
                        user.playernumber = 2
                        currentGame.player2 = user.uid
                        Db.session.add(user)
                        Db.session.add(currentGame)
                        break
                    if p == currentGame.player3: 
                        user.playernumber = 3
                        currentGame.player3 = user.uid
                        Db.session.add(user)
                        Db.session.add(currentGame)
                        break
                    if p == currentGame.player4: 
                        user.playernumber = 4
                        currentGame.player4 = user.uid
                        Db.session.add(user)
                        Db.session.add(currentGame)
                        break
                    if p == currentGame.player5: 
                        user.playernumber = 5
                        currentGame.player5 = user.uid
                        Db.session.add(user)
                        Db.session.add(currentGame)
                        break
                    
                elif p!=emptyProfile and p != testProfile:
                    user.playernumber = 5
                    currentGame.player5 = user.uid
                    Db.session.add(user)
                    Db.session.add(currentGame)

	    	# 	Db.session.add(user)
	    	# 	Db.session.add(currentGame)
	    	# elif currentGame.player3 == emptyProfile and currentGame.player4 != emptyProfile:
	    	# 	currentGame.player3 = user.uid
	    	# 	user.playernumber = 3
	    	# 	Db.session.add(user)
	    	# 	Db.session.add(currentGame)
	    	# elif currentGame.player2 ==emptyProfile and currentGame.player3 != emptyProfile:
	    	# 	currentGame.player2 = user.uid
	    	# 	user.playernumber = 2
	    	# 	Db.session.add(user)
	    	# 	Db.session.add(currentGame)
	    	# elif currentGame.player1 == testProfile: 
	    	# 	currentGame.player1 = user.uid
	    	# 	user.playernumber = 1
	    	# 	Db.session.add(user)
	    	# 	Db.session.add(currentGame)
	    	# else:
	    	# 	currentGame.player5 = user.uid
	    	# 	user.playernumber = 5
	    	# 	Db.session.add(user)
	    	# 	Db.session.add(currentGame)

	    	# assign to session uid
            session['uid'] = user.uid
            Db.session.commit()

        if username == 'ADMIN':
            session['uid'] = adminProfile
            Db.session.commit()

        # list for waiting room
        player1 = User.query.filter_by(uid=currentGame.player1).first()
        player2 = User.query.filter_by(uid=currentGame.player2).first()
        player3 = User.query.filter_by(uid=currentGame.player3).first()
        player4 = User.query.filter_by(uid=currentGame.player4).first()
        player5 = User.query.filter_by(uid=currentGame.player5).first()
        players = [player1, player2, player3, player4, player5] 

        #flash('Congratulations, you have entered a game')
        return render_template('waiting.html', title='Waiting', players = players, session_username=username, session_game =gameID, room = 1)
    else:
        return render_template('signup.html', form = form, title='Enter')  

# GET & POST /removeuser
@app.route('/removeuser', methods=['GET', 'POST'])
def removeuser():

    # Init form
    form = RemoveUserForm()

    session_uid = User.query.filter_by(uid=session['uid']).first()
    session_game = Game.query.filter_by(gid=session['gameID']).first()
    #posts = Post.query.filter_by(author=session_user.uid).all()

    # which waiting room (1-3) for if reconnecting
    if session_uid.response1 is None:
        room = 1
    if session_uid.response1 is not None and session_uid.voting1 is None:
        room = 2
    if session_uid.response1 is not None and session_uid.voting1 is not None:   
        room = 3

    if request.method == 'POST':
        # Get field button values and query vote was for which player's response
        removeuser_entry = int(request.form.get("remove"))
        if removeuser_entry == 1:
            session_game.player1 = emptyProfile
        if removeuser_entry == 2:
            session_game.player2 = emptyProfile
        if removeuser_entry == 3:
            session_game.player3 = emptyProfile
        if removeuser_entry == 4:
            session_game.player4 = emptyProfile
        if removeuser_entry == 5:
            session_game.player5 = emptyProfile
        if removeuser_entry == 6:
            session_game.player6 = emptyProfile

        Db.session.add(session_game)
        Db.session.commit()

        player1 = User.query.filter_by(uid=session_game.player1).first()
        player2 = User.query.filter_by(uid=session_game.player2).first()
        player3 = User.query.filter_by(uid=session_game.player3).first()
        player4 = User.query.filter_by(uid=session_game.player4).first()
        player5 = User.query.filter_by(uid=session_game.player5).first()
        players = [player1, player2, player3, player4, player5] 

        return render_template('waiting.html', title='Waiting', room = 1, players = players, session_username=session_uid.username, session_game=session_game.gid)
    else:
        #all_posts = Post.query.all()
        return render_template('waiting.html', title='Waiting', room = room, players = players, session_username=session_uid.username, session_game=session_game.gid)
   
@app.route('/waiting')
def waiting():
    # Control by login status
    if 'username' in session:
        session_uid = User.query.filter_by(uid=session['uid']).first()
        session_game = Game.query.filter_by(gid=session['gameID']).first()
        #posts = Post.query.filter_by(author=session_user.uid).all()

        # which waiting room (1-3) for if reconnecting
        if session_uid.response1 is None:
        	room = 1
        if session_uid.response1 is not None and session_uid.voting1 is None:
        	room = 2
        if session_uid.response1 is not None and session_uid.voting1 is not None:	
        	room = 3

        return render_template('waiting.html', title='Waiting', room = room, players = [" "], session_username=session_uid.username, session_game=session_game)
    else:
        #all_posts = Post.query.all()
        return render_template('waiting.html', title='Waiting', room = room, players = [" "], session_username=session_uid.username, session_game=session_game)

@app.route('/results', methods=['GET'])
def results():
    # Control by login status
    if 'username' in session:
        session_uid = User.query.filter_by(uid=session['uid']).first()
        session_game = Game.query.filter_by(gid=session['gameID']).first()
        #posts = Post.query.filter_by(author=session_user.uid).all()

        # Get each question and its responses
        # call responses from all users from game
        player1 = User.query.filter_by(uid=session_game.player1).first()
        player2 = User.query.filter_by(uid=session_game.player2).first()
        player3 = User.query.filter_by(uid=session_game.player3).first()
        player4 = User.query.filter_by(uid=session_game.player4).first()
        player5 = User.query.filter_by(uid=session_game.player5).first()
        question1 = Question.query.filter_by(qid = session_game.qid1).first()
        question2 = Question.query.filter_by(qid = session_game.qid2).first()
        question3 = Question.query.filter_by(qid = session_game.qid3).first()
        question4 = Question.query.filter_by(qid = session_game.qid4).first()
        question5 = Question.query.filter_by(qid = session_game.qid5).first()
        players = [player1, player2, player3, player4, player5]
        q1 = [player1.username +": "+ player1.response1, player2.username +": "+ player2.response1, player3.username +": "+ player3.response1, player4.username +": "+ player4.response1, player5.username +": "+ player5.response1, "Correct answer: "+question1.correct]
        q2 = [player1.username +": "+ player1.response2, player2.username +": "+ player2.response2, player3.username +": "+ player3.response2, player4.username +": "+ player4.response2, player5.username +": "+ player5.response2, "Correct answer: "+question2.correct]
        q3 = [player1.username +": "+ player1.response3, player2.username +": "+ player2.response3, player3.username +": "+ player3.response3, player4.username +": "+ player4.response3, player5.username +": "+ player5.response3, "Correct answer: "+question3.correct]
        q4 = [player1.username +": "+ player1.response4, player2.username +": "+ player2.response4, player3.username +": "+ player3.response4, player4.username +": "+ player4.response4, player5.username +": "+ player5.response4, "Correct answer: "+question4.correct]
        q5 = [player1.username +": "+ player1.response5, player2.username +": "+ player2.response5, player3.username +": "+ player3.response5, player4.username +": "+ player4.response5, player5.username +": "+ player5.response5, "Correct answer: "+question5.correct]
        v1 = [player1.voting1, player2.voting1, player3.voting1, player4.voting1, player5.voting1]
        v2 = [player1.voting2, player2.voting2, player3.voting2, player4.voting2, player5.voting2]
        v3 = [player1.voting3, player2.voting3, player3.voting3, player4.voting3, player5.voting3]
        v4 = [player1.voting4, player2.voting4, player3.voting4, player4.voting4, player5.voting4]
        v5 = [player1.voting5, player2.voting5, player3.voting5, player4.voting5, player5.voting5]

        correctVote1 = 0
        correctVote2 = 0
        correctVote3 = 0
        correctVote4 = 0
        correctVote5 = 0
        # your vote 1
        yourVote1 = 0
        if (session_uid.voting1 == 1):
        	yourVote1 = player1.username
        
        if (session_uid.voting1 == 2):
        	yourVote1 = player2.username
        
        if (session_uid.voting1 == 3):
        	yourVote1 = player3.username
        
        if (session_uid.voting1 == 4):
        	yourVote1 = player4.username
        
        if (session_uid.voting1 == 5):
        	yourVote1 = player5.username
        
        if (session_uid.voting1 == 6):
        	yourVote1 = "the correct answer!"
        	correctVote1 = 2

        # who voted for you
        myVotes1 = 0
        myVotesArray1 = []
        myVotesArray1.append(' ')
        for p in players:
        	if p.voting1 == session_uid.playernumber:
        		myVotesArray1.append(p.username)
        		myVotes1 = len(myVotesArray1) -1

		# points calculation
        myPoints1 = myVotes1 + correctVote1
        session_uid.score = myPoints1
        

        # your vote 2
        yourVote2 = 0
        if (session_uid.voting2 == 1):
        	yourVote2 = player1.username
        
        if (session_uid.voting2 == 2):
        	yourVote2 = player2.username
        
        if (session_uid.voting2 == 3):
        	yourVote2 = player3.username
        
        if (session_uid.voting2 == 4):
        	yourVote2 = player4.username
        
        if (session_uid.voting2 == 5):
        	yourVote2 = player5.username
        
        if (session_uid.voting2 == 6):
        	yourVote2 = "the correct answer!"
        	correctVote2 = 2

        # who voted for you
        myVotes2 = 0
        myVotesArray2 = []
        myVotesArray2.append(' ')
        for p in players:
        	if p.voting2 == session_uid.playernumber:
        		myVotesArray2.append(p.username)
        		myVotes2 = len(myVotesArray2) -1

		# points calculation
        myPoints2 = myVotes2 + correctVote2
        session_uid.score = myPoints1 + myPoints2

        # your vote 3
        yourVote3 = 0
        if (session_uid.voting3 == 1):
        	yourVote3 = player1.username
        
        if (session_uid.voting3 == 2):
        	yourVote3 = player2.username
        
        if (session_uid.voting3 == 3):
        	yourVote3 = player3.username
        
        if (session_uid.voting3 == 4):
        	yourVote3 = player4.username
        
        if (session_uid.voting3 == 5):
        	yourVote3 = player5.username
        
        if (session_uid.voting3 == 6):
        	yourVote3 = "the correct answer!"
        	correctVote3 = 2

        # who voted for you
        myVotes3 = 0
        myVotesArray3 = []
        myVotesArray3.append(' ')
        for p in players:
        	if p.voting3 == session_uid.playernumber:
        		myVotesArray3.append(p.username)
        		myVotes3 = len(myVotesArray3) -1

		# points calculation
        myPoints3 = myVotes3 + correctVote3
        session_uid.score = myPoints1 + myPoints2 + myPoints3

        # your vote 4
        yourVote4 = 0
        if (session_uid.voting4 == 1):
        	yourVote4 = player1.username
        
        if (session_uid.voting4 == 2):
        	yourVote4 = player2.username
        
        if (session_uid.voting4 == 3):
        	yourVote4 = player3.username
        
        if (session_uid.voting4 == 4):
        	yourVote4 = player4.username
        
        if (session_uid.voting4 == 5):
        	yourVote4 = player5.username
        
        if (session_uid.voting4 == 6):
        	yourVote4 = "the correct answer!"
        	correctVote4 = 2

        # who voted for you
        myVotes4 = 0
        myVotesArray4 = []
        myVotesArray4.append(' ')
        for p in players:
        	if p.voting4 == session_uid.playernumber:
        		myVotesArray4.append(p.username)
        		myVotes4 = len(myVotesArray4) -1

		# points calculation
        myPoints4 = myVotes4 + correctVote4
        session_uid.score = myPoints1 + myPoints2 + myPoints3 + myPoints4 

        # your vote 5
        yourVote5 = 0
        if (session_uid.voting5 == 1):
        	yourVote5 = player1.username
        
        if (session_uid.voting5 == 2):
        	yourVote5 = player2.username
        
        if (session_uid.voting5 == 3):
        	yourVote5 = player3.username
        
        if (session_uid.voting5 == 4):
        	yourVote5 = player4.username
        
        if (session_uid.voting5 == 5):
        	yourVote5 = player5.username
        
        if (session_uid.voting5 == 6):
        	yourVote5 = "the correct answer!"
        	correctVote5 = 2

        # who voted for you
        myVotes5 = 0
        myVotesArray5 = []
        myVotesArray5.append(' ')
        for p in players:
        	if p.voting5 == session_uid.playernumber:
        		myVotesArray5.append(p.username)
        		myVotes5 = len(myVotesArray5) -1

		# points calculation
        myPoints5 = myVotes5 + correctVote5
        session_uid.score = myPoints1 + myPoints2 + myPoints3 + myPoints4 + myPoints5

        Db.session.add(session_uid)
        Db.session.commit()

        return render_template('results.html', title='Results', myPoints1 = myPoints1, myVotesArray1 = myVotesArray1, myVotes1 = myVotes1, yourVote1 = yourVote1, q1 = q1, question1 = question1.question, myPoints2 = myPoints2, myVotesArray2 = myVotesArray2, myVotes2 = myVotes2, yourVote2 = yourVote2, q2 = q2, question2 = question2.question, myPoints3 = myPoints3, myVotesArray3 = myVotesArray3, myVotes3 = myVotes3, yourVote3 = yourVote3, q3 = q3, question3 = question3.question, myPoints4 = myPoints4, myVotesArray4 = myVotesArray4, myVotes4 = myVotes4, yourVote4 = yourVote4, q4 = q4, question4 = question4.question, myPoints5 = myPoints5, myVotesArray5 = myVotesArray5, myVotes5 = myVotes5, yourVote5 = yourVote5, q5 = q5, question5 = question5.question, session_username=session_uid.username, game=session_game)
    else:
        #all_posts = Post.query.all()
        return render_template('results.html', title='Results', session_username=session_uid.username, game=session_game)

@app.route('/results2', methods=['GET'])
def results2():
    # Control by login status
    if 'username' in session:
        session_uid = User.query.filter_by(uid=session['uid']).first()
        session_game = Game.query.filter_by(gid=session['gameID']).first()
        #posts = Post.query.filter_by(author=session_user.uid).all()

        # Get each question and its responses
        # call responses from all users from game
        player1 = User.query.filter_by(uid=session_game.player1).first()
        player2 = User.query.filter_by(uid=session_game.player2).first()
        player3 = User.query.filter_by(uid=session_game.player3).first()
        player4 = User.query.filter_by(uid=session_game.player4).first()
        player5 = User.query.filter_by(uid=session_game.player5).first()
        players = [player1, player2, player3, player4, player5]

        # display for admin results view
        
        question1 = Question.query.filter_by(qid = session_game.qid1).first()
        question2 = Question.query.filter_by(qid = session_game.qid2).first()
        question3 = Question.query.filter_by(qid = session_game.qid3).first()
        question4 = Question.query.filter_by(qid = session_game.qid4).first()
        question5 = Question.query.filter_by(qid = session_game.qid5).first()
        q1 = [player1.username +": "+ player1.response1, player2.username +": "+ player2.response1, player3.username +": "+ player3.response1, player4.username +": "+ player4.response1, player5.username +": "+ player5.response1, "Correct answer: "+question1.correct]
        q2 = [player1.username +": "+ player1.response2, player2.username +": "+ player2.response2, player3.username +": "+ player3.response2, player4.username +": "+ player4.response2, player5.username +": "+ player5.response2, "Correct answer: "+question2.correct]
        q3 = [player1.username +": "+ player1.response3, player2.username +": "+ player2.response3, player3.username +": "+ player3.response3, player4.username +": "+ player4.response3, player5.username +": "+ player5.response3, "Correct answer: "+question3.correct]
        q4 = [player1.username +": "+ player1.response4, player2.username +": "+ player2.response4, player3.username +": "+ player3.response4, player4.username +": "+ player4.response4, player5.username +": "+ player5.response4, "Correct answer: "+question4.correct]
        q5 = [player1.username +": "+ player1.response5, player2.username +": "+ player2.response5, player3.username +": "+ player3.response5, player4.username +": "+ player4.response5, player5.username +": "+ player5.response5, "Correct answer: "+question5.correct]
         
        # points calculation
        highPlayerScore = 0
        highPlayer=[]
        tie = False
        for p in players:
        	if p.score is None:
        		p.score = 0
        	if p.score > highPlayerScore:
        		highPlayerScore = p.score # find high score
        for p in players: # find ties
        	if p.score == highPlayerScore:
        		highPlayer.append(p.username)
        if len(highPlayer) >1:
        	tie = True

        # create response button names
        #responseButtons = ["resp1-1", "resp1-2", "resp1-3", "resp1-4", "resp1-5", "resp1-6"; "resp2-1", "resp2-2", "resp2-3", "resp2-4", "resp2-5", "resp2-6"; "resp3-1", "resp3-2", "resp3-3", "resp3-4", "resp3-5", "resp3-6"; "resp4-1", "resp4-2", "resp4-3", "resp4-4", "resp4-5", "resp4-6"; "resp5-1", "resp5-2", "resp5-3", "resp5-4", "resp5-5", "resp5-6"] 
		
        
        return render_template('results2.html', title='Results', question1 = question1, question2 = question2, question3 = question3, question4 = question4, question5 = question5, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, tie = tie, highPlayerScore = highPlayerScore, highPlayer = highPlayer, players = players, session_username=session_uid.username, game=session_game)
    else:
        #all_posts = Post.query.all()
        return render_template('results2.html', title='Results', session_username=session_uid.username, game=session_game)


# POST /logout
@app.route('/logout', methods=['POST'])
def logout():
    # Logout
    session.clear()
    return redirect(url_for('enter'))


# GET & POST /play
@app.route('/play', methods=['GET', 'POST'])
def play():
    # Init form
    form = PlayForm()

    # Init user by Db query to user and to game?
    #user = User.query.filter_by(username=username).first()
    session_user = User.query.filter_by(uid=session['uid']).first()
    session_game = Game.query.filter_by(gid=session['gameID']).first()

    question1 = Question.query.filter_by(qid = session_game.qid1).first()
    question2 = Question.query.filter_by(qid = session_game.qid2).first()
    question3 = Question.query.filter_by(qid = session_game.qid3).first()
    question4 = Question.query.filter_by(qid = session_game.qid4).first()
    question5 = Question.query.filter_by(qid = session_game.qid5).first()

    if request.method == 'POST':
        # Init credentials from form request
        session_user.response1 = request.form['response1']
        if question2.question != 'blank':
        	session_user.response2 = request.form['response2']
        if question3.question != 'blank':
        	session_user.response3 = request.form['response3']
        if question4.question != 'blank':
        	session_user.response4 = request.form['response4']
        if question5.question != 'blank':
        	session_user.response5 = request.form['response5']

        if session['uid'] != adminProfile:
        	Db.session.add(session_user)
        	Db.session.commit()

        # show players to player1 waiting room?
        player1 = User.query.filter_by(uid=session_game.player1).first()
        player2 = User.query.filter_by(uid=session_game.player2).first()
        player3 = User.query.filter_by(uid=session_game.player3).first()
        player4 = User.query.filter_by(uid=session_game.player4).first()
        player5 = User.query.filter_by(uid=session_game.player5).first()
        players = [player1, player2, player3, player4, player5]

        return render_template('waiting.html', title='Play', session_game = session_game.gid,players = players, session_username=session_user.username, form = form, room = 2)
    else:
        
        return render_template('play.html', title='Play', game = session_game, question1=question1.question, question2=question2.question, question3=question3.question, question4=question4.question, question5=question5.question, session_username=session_user.username, form = form)


# GET & POST /voting
@app.route('/voting', methods=['GET', 'POST'])
def voting():
    # Init form
    form = VoteForm()

    # Init user by Db query to user and to game?
    #user = User.query.filter_by(username=username).first()
    session_user = User.query.filter_by(uid=session['uid']).first()
    session_game = Game.query.filter_by(gid=session['gameID']).first()

    # call responses from all users from game and set to default empty player if not found
    player1 = User.query.filter_by(uid=session_game.player1).first()
    player2 = User.query.filter_by(uid=session_game.player2).first()
    player3 = User.query.filter_by(uid=session_game.player3).first()
    player4 = User.query.filter_by(uid=session_game.player4).first()
    player5 = User.query.filter_by(uid=session_game.player5).first()
    players = [player1, player2, player3, player4, player5]
    playerCount=0
    for p in players:
    	if p.username != 'empty':
    		playerCount=playerCount+1
    question1 = Question.query.filter_by(qid = session_game.qid1).first()
    question2 = Question.query.filter_by(qid = session_game.qid2).first()
    question3 = Question.query.filter_by(qid = session_game.qid3).first()
    question4 = Question.query.filter_by(qid = session_game.qid4).first()
    question5 = Question.query.filter_by(qid = session_game.qid5).first()
    q1 = np.array([[1,player1.response1], [2,player2.response1], [3,player3.response1], [4,player4.response1], [5,player5.response1], [6,question1.correct]])
    q2 = np.array([[1,player1.response2], [2,player2.response2], [3,player3.response2], [4,player4.response2], [5,player5.response2], [6,question2.correct]])
    q3 = np.array([[1,player1.response3], [2,player2.response3], [3,player3.response3], [4,player4.response3], [5,player5.response3], [6,question3.correct]])
    q4 = np.array([[1,player1.response4], [2,player2.response4], [3,player3.response4], [4,player4.response4], [5,player5.response4], [6,question4.correct]])
    q5 = np.array([[1,player1.response5], [2,player2.response5], [3,player3.response5], [4,player4.response5], [5,player5.response5], [6,question5.correct]])
    
    # get rid of empties
    q1 = q1[~(q1[:,1] =='blank'),:]
    q2 = q2[~(q2[:,1] =='blank'),:]
    q3 = q3[~(q3[:,1] =='blank'),:]
    q4 = q4[~(q4[:,1] =='blank'),:]
    q5 = q5[~(q5[:,1] =='blank'),:]

    # random by game seed
    gameSeed = session_game.seed
    np.random.seed(gameSeed)
    np.random.shuffle(q1)
    np.random.shuffle(q2)
    np.random.shuffle(q3)
    np.random.shuffle(q4)
    np.random.shuffle(q5)

    # get rid of extra column
    q1resp = q1[:,1]
    q2resp = q2[:,1]
    q3resp = q3[:,1]
    q4resp = q4[:,1]
    q5resp = q5[:,1]

    if request.method == 'POST':
        # Get field button values and query vote was for which player's response
        vote1 = int(request.form.get("voting1", None))
        if question2.question != 'blank':
        	vote2 = int(request.form.get("voting2", None))
        if question3.question != 'blank':
        	vote3 = int(request.form.get("voting3", None))
        if question4.question != 'blank':
        	vote4 = int(request.form.get("voting4", None))
        if question5.question != 'blank':
        	vote5 = int(request.form.get("voting5", None))
        
        session_user.voting1 = q1[vote1-1,0]
        if question2.question != 'blank':
        	session_user.voting2 = q2[vote2-1,0]
        if question3.question != 'blank':
        	session_user.voting3 = q3[vote3-1,0]
        if question4.question != 'blank':
        	session_user.voting4 = q4[vote4-1,0]
        if question5.question != 'blank':
        	session_user.voting5 = q5[vote5-1,0]

        if session['uid'] != adminProfile:
            Db.session.add(session_user)
            Db.session.commit()
        return render_template('waiting.html', title='Voting', playerCount = playerCount, players = players, session_game = session_game.gid, session_username=session_user.username, form = form, room = 3)

        # return render_template('waiting.html', title='Voting', game = session_game, session_username=session_user.username, form = form, room = 3)
    else:
        return render_template('voting.html', title='Voting', playerCount = playerCount,question1 = question1.question, question2 = question2.question, question3 = question3.question, question4 = question4.question,question5 = question5.question,q1=q1resp, q2=q2resp, q3=q3resp, q4=q4resp,q5=q5resp, game = session_game, session_username=session_user.username, form = form)


# GET & POST /create
@app.route('/create', methods=['GET', 'POST'])
def create():
    # Init form
    form = CreateGame()

    if request.method == 'POST':
    	# is the current empty uid
    	# create random seed int
    	numberQuestions = int(request.form.get("numberQuestions"))
    	adminAccess = int(request.form.get("adminResults"))
    	randomSeed = np.random.randint(100)
    	game = Game(player1=testProfile, player2=emptyProfile, player3=emptyProfile, player4=emptyProfile, player5=emptyProfile, seed = randomSeed, admin = adminAccess)
    	Db.session.add(game)
    	Db.session.commit()

    	newGame = Game.query.order_by(-Game.gid).first() # can use just game?
    	# fill array with random question
    	# shuffle
    	newQuestions = Question.query.order_by(func.random())[:5]
    	# place in newGame column
    	if numberQuestions >= 1:
    		newGame.qid1 = newQuestions[0].qid
    	if numberQuestions >= 2: 
    		newGame.qid2 = newQuestions[1].qid
    	else:
    		newGame.qid2 = blankQuestion
    	if numberQuestions >= 3:
    		newGame.qid3 = newQuestions[2].qid
    	else:
    		newGame.qid3 = blankQuestion
    	if numberQuestions >= 4:
    		newGame.qid4 = newQuestions[3].qid
    	else:
    		newGame.qid4 = blankQuestion
    	if numberQuestions >= 5:
    		newGame.qid5 = newQuestions[4].qid
    	else:
    		newGame.qid5 = blankQuestion

    	Db.session.add(game)
    	Db.session.commit()
    	flash('Congratulations, you have created a new game! You can now login with a username. Here is your Game ID:')
    	return render_template('index.html', form = form, title='Create', games = newGame)
    else:
    	#all_games = Game.query.all()
    	return render_template('index.html', form = form, title='Create', games = 0)
  
