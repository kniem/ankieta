from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from datetime import datetime
import statistics
#import os
import psycopg2



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
heroku=Heroku(app)
db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    age=db.Column(db.Integer)
    ans1=db.Column(db.Integer)
    ans1test=db.Column(db.Integer)
    ans2=db.Column(db.Integer)
    ans2test=db.Column(db.Integer)
    ans3=db.Column(db.Integer)
    ans3test=db.Column(db.Integer)
    ans4=db.Column(db.Integer)
    ans4test=db.Column(db.Integer)
    ans5=db.Column(db.Integer)
    ans5test=db.Column(db.Integer)
    ans6=db.Column(db.Integer)
    ans6test=db.Column(db.Integer)
    ans7=db.Column(db.Integer)
    ans7test=db.Column(db.Integer)
    ans8=db.Column(db.Integer)
    ans8test=db.Column(db.Integer)
    ans9=db.Column(db.Integer)
    ans9test=db.Column(db.Integer)
    ans10=db.Column(db.Integer)
    ans10test=db.Column(db.Integer)


    def __init__(ans1, ans1test, ans2, ans2test, ans3, ans3test, ans4, ans4test, ans5, ans5test, ans6, ans6test, ans7, ans7test, ans8, ans8test, ans9, ans9test, ans10, ans10test):
        self.ans1 =ans1
        self.ans1test=ans1test
        self.ans2=ans2
        self.ans2test=ans2test
        self.ans3=ans3
        self.ans3test=ans3test
        self.ans4=ans4
        self.ans4test=ans4test
        self.ans5=ans5
        self.ans5test=ans5test
        self.ans6=ans6
        self.ans6test=ans6test
        self.ans7=ans7
        self.ans7test=ans7test
        self.ans8=ans8
        self.ans8test=ans8test
        self.ans9=ans9
        self.ans9test=ans9test
        self.ans10=ans10
        self.ans10test=ans10test

db.create_all()


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/form")
def show_form():
    return render_template('form.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    #wszystkie wyniki z bazy to fd_list
    fd_list = db.session.query(Formdata).all()

    #range1: do 20, 2: 20-30, 3: 30-40, 4: 40+
    #odpowiedzi: nie znam - 0, znam - 1
    #odpowiedzi: zle: 0, dobrze 1

    
    age1=Formatdata.query.filter_by(age=1)
    age2=Formatdata.query.filter_by(age=2)
    age3=Formatdata.query.filter_by(age=2)
    age4=Formatdata.query.filter_by(age=2)

    

    # Some simple statistics for sample questions
    # satisfaction = []
    # q1 = []
    # q2 = []
    # for el in fd_list:
    #     satisfaction.append(int(el.satisfaction))
    #     q1.append(int(el.q1))
    #     q2.append(int(el.q2))

    # if len(satisfaction) > 0:
    #     mean_satisfaction = statistics.mean(satisfaction)
    # else:
    #     mean_satisfaction = 0

    # if len(q1) > 0:
    #     mean_q1 = statistics.mean(q1)
    # else:
    #     mean_q1 = 0

    # if len(q2) > 0:
    #     mean_q2 = statistics.mean(q2)
    # else:
    #     mean_q2 = 0

    # Prepare data for google charts
    data = [['Satisfaction', mean_satisfaction], ['Python skill', mean_q1], ['Flask skill', mean_q2]]

    return render_template('result.html', data=data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    firstname = request.form['firstname']
    email = request.form['email']
    age = request.form['age']
    income = request.form['income']
    satisfaction = request.form['satisfaction']
    q1 = request.form['q1']
    q2 = request.form['q2']

    # Save the data
    fd = Formdata(firstname, email, age, income, satisfaction, q1, q2)
    db.session.add(fd)
    db.session.commit()

    return redirect ("/")


if __name__ == "__main__":
    app.debug = True
    app.run()
