from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

Db = SQLAlchemy()


class Game(Db.Model):
    __tablename__ = 'games'
    gid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    player1 = Db.Column(Db.String(64))
    player2 = Db.Column(Db.String(64))
    player3 = Db.Column(Db.String(64))
    player4 = Db.Column(Db.String(64))
    player5 = Db.Column(Db.String(64))
    qid1 = Db.Column(Db.Integer)
    qid2 = Db.Column(Db.Integer)
    qid3 = Db.Column(Db.Integer)
    qid4 = Db.Column(Db.Integer)
    qid5 = Db.Column(Db.Integer)
    seed = Db.Column(Db.Integer)
    admin = Db.Column(Db.Integer)
    

class User(Db.Model):
    __tablename__ = 'users'
    uid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    username = Db.Column(Db.String(64), nullable=False)
    response1 = Db.Column(Db.Text())
    response2 = Db.Column(Db.Text())
    response3 = Db.Column(Db.Text())
    response4 = Db.Column(Db.Text())
    response5 = Db.Column(Db.Text())
    voting1 = Db.Column(Db.Integer)
    voting2 = Db.Column(Db.Integer)
    voting3 = Db.Column(Db.Integer)
    voting4 = Db.Column(Db.Integer)
    voting5 = Db.Column(Db.Integer)
    playernumber = Db.Column(Db.Integer)
    score = Db.Column(Db.Integer)

class Question(Db.Model):
    __tablename__ = 'questions'
    #uid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
    qid = Db.Column(Db.Integer)
    question = Db.Column(Db.Text(), primary_key=True, unique =True, nullable=False)
    correct = Db.Column(Db.Text(), nullable=False)


# class Post(Db.Model):
#     __tablename__ = 'posts'
#     pid = Db.Column(Db.Integer, primary_key=True, autoincrement=True)
#     author = Db.Column(Db.String(64), Db.ForeignKey('users.uid'), nullable=False)
#     content = Db.Column(Db.String(1024), nullable=False)
#     post_date = Db.Column(Db.Date, default=func.now())
#     authorname = Db.relationship(User, backref='posts')

