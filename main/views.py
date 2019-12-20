from flask import request, redirect, url_for, render_template, flash, session, jsonify
from main import app, db
from main.models import User, Date, Proken
import datetime

def save_user(user_name):
    user = User(name = user_name)
    db.session.add(user)
    db.session.commit()
    print("save new user:", user_name)
    flash("save new user successfully")

def make_attend_msg(user_id):
    message = "Attend now!!"

    if User.query.filter_by(id=user_id).first().active:
        message = "Finish work"

    return message

def count_user():
    count = 0
    today = datetime.datetime.today()
    today = str(today.year)+str(today.month)+str(today.day)
    dates = Date.query.filter().all()
    for date in dates:
        user = User.query.filter_by(id=date.user_id).first()
        date = date.start
        date = str(date.year)+str(date.month)+str(date.day)
        if date == today:
            count+=1
            print(user, date)
    return count

def calc_time_diff(t1, t2):
    td = t2 - t1
    return int(td.seconds / 3600)

def make_record(user_id):
    record = {}
    for date in Date.query.filter_by(user_id=user_id).all():
        if date.end is None:
            continue
        record.setdefault(int(date.start.timestamp()), calc_time_diff(date.start, date.end))

    return record

def make_proken():
    record = {}
    for proken in Proken.query.all():
        if proken is None:
            continue
        else :
            record.setdefault(int(proken.day.timestamp()), proken.prokens)
                
    return record


def get_seven_data(user_id):
    user = User.query.filter_by(id=user_id).first()
    dates = user.dates
    start_times = []
    for st in dates:
        start_times.append(st.start)

    start_times = sorted(start_times, reverse=True)

    return start_times[:7]

def decide_sound_level(start_times):
    sound_level = 1
    date = start_times[0]
    for i in (range(1, 7)):
        if start_times[i].date() == date.date() - datetime.timedelta(days=1):
            date = start_times[i]
            sound_level += 1
        else:
            break
    return sound_level

@app.route('/')
def index():
    active_users = User.query.filter_by(active=True).all()
    all_user_num = 4#count_user()
    return render_template('index.html', users=active_users, users_num=all_user_num )

@app.route('/users/create', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        user_name = request.form['user_name']

        if user_name == "" :
            return render_template('new_user.html')
        else :
            save_user(user_name)
            return redirect(url_for('index'))
    return render_template('new_user.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.filter_by(id=user_id).first()
    record = make_record(user_id)
    return render_template('user_detail.html', user = user, record=record)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user_name = request.form['user_name']
        if user_name == "" :
            return render_template('user_edit.html', user = user)
        else :
            user.name = request.form['user_name']
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user_detail', user_id = user.id))

    return render_template('user_edit.html', user = user)

@app.route('/users/')
def user_list():
    users = User.query.all()
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)
    proken = Proken.query.filter_by(day=today).first()
    if proken is None:
        proken = Proken(day=today, prokens=1)
    else:
        proken.prokens += 1

    record = make_proken()

    db.session.add(proken)
    db.session.commit()
    return render_template('user_list.html', users=users, record=record)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.authenticate(db.session.query,
                request.form['user_name'])
        if user != None:
            session['user_id'] = user.id
            flash('You were logged in')
            return redirect(url_for('index'))
        else:
            flash('Invalid your name')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/attend', methods=['GET', 'POST'])
def attend():
    if request.method == 'POST':
        now = datetime.datetime.today()
        date = Date(user_id=session['user_id'], start=now)
        user = User.query.filter(User.id==session['user_id']).first()
        user.active = not user.active
        db.session.add(date)
        db.session.add(user)
        db.session.commit()

        print("Date saved!")
        flash("Thank You !!")
        return redirect(url_for('index'))
    
    message = make_attend_msg(session['user_id'])
    
    return render_template('attend.html', message=message)

@app.route('/raspi/<int:user_id>', methods=['GET', 'POST'])
def raspy(user_id):
    user = User.query.filter_by(id=user_id).first()
    time = datetime.datetime.today()
    if user.active:
        date = Date.query.filter_by(user_id=user_id).first()
        date.end = time
    else:
        date = Date(user_id=user_id, start=time)

    user.active = not user.active
    db.session.add(user)
    db.session.add(date)
    db.session.commit()

    record={
            'user_id' : user_id,
            'date' : str(datetime.date.today() + datetime.timedelta(days=1)),
            'sound' : decide_sound_level( get_seven_data(user_id))
            }

    return jsonify(record)

