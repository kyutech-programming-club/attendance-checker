from flask import request, redirect, url_for, render_template, flash
from main import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/create', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':

        if request.form['user_name'] == "" :
            return render_template('new_user.html')
        else :
            return redirect(url_for('index'))
    return render_template('new_user.html')
