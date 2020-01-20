from flask import request, redirect, url_for, render_template, flash, session, jsonify
from main import app, db
from main.models import User, Date, Time
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

def get_today():
    today_date = datetime.date.today()
    today = datetime.datetime(*today_date.timetuple()[:3])

    return today

def new_date_make(date):
    new_date = Date(day=date, members=0)
    db.session.add(new_date)
    db.session.commit()

def count_member():
    today = get_today()
    member_num = 0
    date = Date.query.filter_by(day=today).first()

    if date is None :
        new_date_make()
    else :
        member_num = date.members

    return member_num

def calc_time_diff(start, end):
    time_diff = end - start
    return int(time_diff.seconds / 3600)

def get_date(datetime_obj):
    date = datetime.datetime(*datetime_obj.timetuple()[:3])
    return date

def user_record_maker(user_id):
    record = {}
    user = User.query.filter_by(user_id=user_id).first()
    times = Time.query.filter_by(user_id=user_id).all()

    for time in times :
        date = get_date(time.start)
        work_time = calc_time_diff(time.start, time.end)
        
        record.setdefault(int(date.timestamp()), work_time)

    return record

def proken_record_maker():
    record = {}
    for date in Date.query.all():
        record.setdefault(int(date.day.timestamp()), date.members)
                
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
    all_user_num = count_member()
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
    user = User.query.filter_by(user_id=user_id).first()
    record = user_record_maker(user_id)
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
    record = proken_record_maker()

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

