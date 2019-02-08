# -*- coding: utf-8 -*-
# quiz-orm/views.py
from datetime import datetime

from flask import Flask, flash, redirect, url_for, request
from flask import render_template

from uczniowie.forms import KlasaForm
from uczniowie.modele import Klasa

app = Flask(__name__)


@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')


def lata(a, b):
  rok = datetime.now().year
  lata = []
  for i in range(a, b):
    lata.append((rok - i, rok - i))

  return lata


@app.route("/dodaj_klase", methods=['GET', 'POST'])
def dodaj_klase():
  form = KlasaForm()

  form.rok_naboru.choices = lata(-1, 10)
  form.rok_matury.choices = lata(-4, 7)

  if form.validate_on_submit():
    print(form.data)
    p = Klasa(nazwa=form.nazwa.data,
              rok_naboru=form.rok_naboru.data, rok_matury=form.rok_matury.data)
    p.save()
    flash("Dodano klasę: {}".format(form.nazwa.data))
    return redirect(url_for('index'))

  elif request.method == 'POST':
    pass
    # TODO Show errrors
    # flash_errors(form)
  return render_template('dodaj_klase.html', form=form)
