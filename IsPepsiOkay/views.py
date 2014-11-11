from IsPepsiOkay import app, database
from flask import render_template, redirect, request, url_for

@app.route('/')
def index():
    return render_template('index.html')
