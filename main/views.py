from flask import request, redirect, url_for, render_template, flash
from main import app

@app.route('/')
def index():
    return render_template('index.html')
