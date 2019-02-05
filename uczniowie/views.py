# -*- coding: utf-8 -*-
# quiz-orm/views.py

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')

