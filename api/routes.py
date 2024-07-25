from flask import render_template
from . import app

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/pages/profile')
def about():
    return render_template('profile.html')
