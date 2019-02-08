# -*- coding: utf-8 -*-
# quiz-orm/views.py

from flask import Flask, flash, redirect, url_for, request
from flask import render_template

from uczniowie.forms import KlasaForm

app = Flask(__name__)

@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')


@app.route("/dodaj_klase", methods=['GET', 'POST'])
def dodaj_klase():
  form = KlasaForm()

  if form.validate_on_submit():
    print(form.data)
    p = KlasaForm(pytanie=form.pytanie.data, kategoria=form.kategoria.data)
    p.save()
    flash("Dodano klase: {}".format(form.nazwa.data))
    return redirect(url_for('index'))

  elif request.method == 'POST':
    pass
    # TODO Show errrors
    # flash_errors(form)
