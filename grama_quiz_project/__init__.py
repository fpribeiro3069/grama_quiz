import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flask import (
    render_template, request, session, url_for
)

app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
    #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    SQLALCHEMY_DATABASE_URI='sqlite:///gramaquiz.sqlite3'
)

db = SQLAlchemy(app)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f'Team {self.name}'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Answers requiring free text
    text = db.Column(db.String(100), nullable=True)

    # Multiple choice answers
    choice = db.Column(db.Integer, nullable=True)

    questionId = db.Column(db.Integer, nullable=False)
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def __repr__(self):
        return f'Team {self.teamId} answer to question {self.questionId}:\n{self.text}'

# a simple page that says hello
@app.route("/")
def hello_world():
    return render_template('HomePage.html')

@app.route("/team", methods=['POST'])
def team():
    data = request.form

    name = data['name']
    team = Team(name=name)

    db.session.add(team)
    db.session.commit()

    return render_template('Questions.html', teamId=team.id)

@app.route('/questions', methods=['GET'])
def questions():
    return render_template('Questions.html')

@app.route("/<teamId>/questions/<questionId>", methods=['GET', 'POST'])
def answer(teamId, questionId):
    if request.method == 'GET':
        return render_template('Answer.html', teamId=teamId, questionId=questionId)

    create = False

    previousAnswer = Answer.query.filter_by(teamId=teamId, questionId=questionId).first()
    if not previousAnswer:
        create = True
        previousAnswer = Answer(teamId=teamId, questionId=questionId)

    data = request.form
    print(data)
    # previousAnswer.choice = data['choice']
    previousAnswer.text = data['text']

    if create:
        db.session.add(previousAnswer)

    db.session.commit()

    return None