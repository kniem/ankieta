from flask import Flask, render_template, request, redirect, flash, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.session import Session
from flask.ext.heroku import Heroku
from datetime import datetime
import statistics
#import os
#import psycopg2

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()
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


def index_min(values):
    return min(range(len(values)),key=values.__getitem__)


def index_max(values):
    return max(range(len(values)),key=values.__getitem__)


def min_string(values):
    group_vector = ['do 15 lat', 'od 16 do 25 lat', 'od 26 do 35 lat', 'od 36 do 45 lat', 'powyżej 46 lat']
    i_min = index_min(values)
    age_string = str(group_vector[i_min])
    score_string = str(format(values[i_min], '.2f'))
    return age_string, score_string


def max_string(values):
    group_vector = ['do 15 lat', 'od 16 do 25 lat', 'od 26 do 35 lat', 'od 36 do 45 lat', 'powyżej 46 lat']
    i_max = index_max(values)
    age_string = str(group_vector[i_max])
    score_string = str(format(values[i_max], '.2f'))
    return age_string, score_string


def count_answers(arr):
    return [['0 pkt', arr.count(0)], ['1 pkt', arr.count(1)], ['2 pkt', arr.count(2)]]


def check_answer(answer, correct_answer):
    if answer == correct_answer:
        return 1
    else:
        return 0


def mean_in_groups(ages, scores):
    aggregates = [0, 0, 0, 0, 0]
    tallies = [0, 0, 0, 0, 0]
    for index in range(len(ages)):
        tallies[ages[index]-1] += 1
        aggregates[ages[index]-1] += scores[index]
    for index in range(len(aggregates)):
        if tallies[index] != 0:
            aggregates[index] /= tallies[index]
    means = aggregates
    return means


def mean_in_language(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    answers = len(q1)
    english = (sum(q1) + sum(q2) + sum(q3) + sum(q4) + sum(q5))/answers
    polish = (sum(q6) + sum(q7) + sum(q8) + sum(q9) + sum(q10))/answers
    means = [round(english, 2), round(polish, 2)]
    return means


def tough_easy_questions(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    total_points = [sum(q1), sum(q2), sum(q3), sum(q4), sum(q5), sum(q6), sum(q7), sum(q8), sum(q9), sum(q10)]
    toughest_q = index_min(total_points)
    easiest_q = index_max(total_points)
    q_list = ['ASAP', 'TL;DR', 'DM me', 'IDK', 'ELI5', 'NMZC', 'JBC', 'JJ', 'OCB', 'ZW']
    toughest_pts = str(format(total_points[toughest_q], '.2f'))
    easiest_pts = str(format(total_points[easiest_q], '.2f'))
    return q_list[toughest_q], toughest_pts, q_list[easiest_q], easiest_pts


@app.route("/")
def welcome():
    fd_list = db.session.query(Formdata).all()
    fd_list_older = db.session.query(Formdata).filter((Formdata.age == '4') | (Formdata.age == '5')).all()
    score = 0
    rows = 0
    for el in fd_list:
        score += (int(el.q1) + int(el.q2) + int(el.q3) + int(el.q4) + int(el.q5) + int(el.q6) + int(el.q7) +
                      int(el.q8) + int(el.q9) + int(el.q10))
        rows += 1
    mean_score = format(score/rows, '.2f')
    rows = 0
    score = 0

    for el in fd_list_older:
        score += (int(el.q1) + int(el.q2) + int(el.q3) + int(el.q4) + int(el.q5) + int(el.q6) + int(el.q7) +
                  int(el.q8) + int(el.q9) + int(el.q10))
        rows += 1
    older_score = format(score/rows, '.2f')

    participants = db.session.query(Formdata).count()
    return render_template('welcome.html', no_of_participants=participants, mean=mean_score,
                           older_mean=older_score)

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
    score = []

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
        score.append((int(el.q1) + int(el.q2) + int(el.q3) + int(el.q4) + int(el.q5) + int(el.q6) + int(el.q7) +
                        int(el.q8) + int(el.q9) + int(el.q10)))

    age_data = ([['<=15', age.count(1), '16-25', age.count(2), '26-35', age.count(3), '36-45',
                  age.count(4), '>=46', age.count(5)]])

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

    mean_data_vector = mean_in_groups(age, score)
    mean_data_lang_vector = mean_in_language(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
    max_string_result = max_string(mean_data_vector)
    min_string_result = min_string(mean_data_vector)
    t_e_strings = tough_easy_questions(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
    mean_data = ([['<=15', mean_data_vector[0]], ['16-25', mean_data_vector[1]], ['26-35', mean_data_vector[2]],
                 ['36-45', mean_data_vector[3]], ['>=46', mean_data_vector[4]]])
    mean_data_lang = [['Angielskie', mean_data_lang_vector[0]], ['Polskie', mean_data_lang_vector[1]]]

    return render_template('result.html', q1_data=q1_data, q2_data=q2_data, q3_data=q3_data, q4_data=q4_data,
                           q5_data=q5_data, q6_data=q6_data, q7_data=q7_data, q8_data=q8_data, q9_data=q9_data,
                           q10_data=q10_data, mean_data=mean_data, max_string_result=max_string_result,
                           min_string_result=min_string_result, mean_data_lang=mean_data_lang,
                           t_e_strings=t_e_strings)


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
    age = request.form['age']
    q1 = int(request.form['q1'])
    if q1:
        q1 *= check_answer(request.form['ans1test'], 'a')

    q2 = int(request.form['q2'])
    if q2:
        q2 *= check_answer(request.form['ans2test'], 'c')

    q3 = int(request.form['q3'])
    if q3:
        q3 *= check_answer(request.form['ans3test'], 'c')

    q4 = int(request.form['q4'])
    if q4:
        q4 *= check_answer(request.form['ans4test'], 'a')

    q5 = int(request.form['q5'])
    if q5:
        q5 *= check_answer(request.form['ans5test'], 'b')

    q6 = int(request.form['q6'])
    if q6:
        q6 *= check_answer(request.form['ans6test'], 'b')

    q7 = int(request.form['q7'])
    if q7:
        q7 *= check_answer(request.form['ans7test'], 'a')

    q8 = int(request.form['q8'])
    if q8:
        q8 *= check_answer(request.form['ans8test'], 'c')

    q9 = int(request.form['q9'])
    if q9:
        q9 *= check_answer(request.form['ans9test'], 'b')

    q10 = int(request.form['q10'])
    if q10:
        q10 *= check_answer(request.form['ans10test'], 'c')

    # Save the data
    fd = Formdata(age, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)
    db.session.add(fd)
    db.session.commit()
    flash('DZIĘKUJEMY! Twoje odpowiedzi zostały przesłane do bazy danych')
    return redirect(url_for('welcome'))



if __name__ == "__main__":

    app.debug = True
    app.run()
