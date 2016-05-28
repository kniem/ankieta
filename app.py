from flask import Flask, render_template, request, redirect, flash, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from datetime import datetime
import statistics
#import os
#import psycopg2

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
heroku=Heroku(app)
db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'poll_data'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    age = db.Column(db.Integer, nullable=False)
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    q8 = db.Column(db.Integer)
    q9 = db.Column(db.Integer)
    q10 = db.Column(db.Integer)

    def __init__(self, age, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
        self.age = age
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.q6 = q6
        self.q7 = q7
        self.q8 = q8
        self.q9 = q9
        self.q10 = q10

db.create_all()

def count_answers(arr):
    return [['Nie mam pojęcia', arr.count(0)], ['Jednak nie wiem', arr.count(1)], ['Wiem', arr.count(2)]]

def check_answer(answer, correct_answer):
    if answer == correct_answer:
        return 1
    else:
        return 0

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
    fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
    age = []
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    q5 = []
    q6 = []
    q7 = []
    q8 = []
    q9 = []
    q10 = []

    for el in fd_list:
        age.append(int(el.age))
        q1.append(int(el.q1))
        q2.append(int(el.q2))
        q3.append(int(el.q3))
        q4.append(int(el.q4))
        q5.append(int(el.q5))
        q6.append(int(el.q6))
        q7.append(int(el.q7))
        q8.append(int(el.q8))
        q9.append(int(el.q9))
        q10.append(int(el.q10))


    age_data = [['<=15', age.count(1), '16-25', age.count(2), '26-35', age.count(3), '36-45', age.count(4), '>=46', age.count(5)]]
    q1_data = count_answers(q1)
    q2_data = count_answers(q2)
    q3_data = count_answers(q3)
    q4_data = count_answers(q4)
    q5_data = count_answers(q5)
    q6_data = count_answers(q6)
    q7_data = count_answers(q7)
    q8_data = count_answers(q8)
    q9_data = count_answers(q9)
    q10_data = count_answers(q10)

    return render_template('result.html', q1_data=q1_data)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    age = request.form['age']
    q1 = int(request.form['q1'])
    if q1:
        q1 = q1 * check_answer(request.form['ans1test'], 'a')

    q2 = int(request.form['q2'])
    if q2:
        q2 = q2 * check_answer(request.form['ans2test'], 'c')

    q3 = int(request.form['q3'])
    if q3:
        q3 = q3 * check_answer(request.form['ans3test'], 'c')

    q4 = int(request.form['q4'])
    if q4:
        q4 = q4 * check_answer(request.form['ans4test'], 'a')

    q5 = int(request.form['q5'])
    if q5:
        q5 = q5 * check_answer(request.form['ans5test'], 'b')

    q6 = int(request.form['q6'])
    if q6:
        q6 = q6 * check_answer(request.form['ans6test'], 'b')

    q7 = int(request.form['q7'])
    if q7:
        q7 = q7 * check_answer(request.form['ans7test'], 'a')

    q8 = int(request.form['q8'])
    if q8:
        q8 = q8 * check_answer(request.form['ans8test'], 'c')

    q9 = int(request.form['q9'])
    if q9:
        q9 = q9 * check_answer(request.form['ans9test'], 'b')

    q10 = int(request.form['q10'])
    if q10:
        q10 = q10 * check_answer(request.form['ans10test'], 'c')

    # Save the data
    fd = Formdata(age, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
    db.session.add(fd)
    db.session.commit()
    flash('<strong>Dziękujemy</strong> za udział w ankiecie! Miłego dnia!')
    return redirect (url_for('welcome'))



if __name__ == "__main__":

    app.debug = True
    app.run()
