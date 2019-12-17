from flask import request, redirect, url_for, render_template, flash, session
from main import app, db
from main.models import User

def save_user(user_name):
    user = User(name = user_name)
    db.session.add(user)
    db.session.commit()
    print("save new user:", user_name)
    flash("save new user successfully")

@app.route('/')
def index():
    return render_template('index.html')

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
    user = User.query.get(user_id)
    return render_template('user_detail.html', user = user)

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
