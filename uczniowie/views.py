# -*- coding: utf-8 -*-
# quiz-orm/views.py
from datetime import datetime
from os import abort

from flask import Flask, flash, redirect, url_for, request
from flask import render_template

from forms import KlasaForm
from modele import *

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
    klasa = Klasa(nazwa=form.nazwa.data,
                  rok_naboru=form.rok_naboru.data, rok_matury=form.rok_matury.data)
    klasa.save()
    flash("Dodano klasę: {}".format(form.nazwa.data))
    return redirect(url_for('index'))

  elif request.method == 'POST':
    pass
    # TODO Show errrors
    # flash_errors(form)
  return render_template('dodaj_klase.html', form=form)


def get_klasa_or_404(klasa_id):
  try:
    klasa = Klasa.get_by_id(klasa_id)
    return klasa
  except Klasa.DoesNotExist:
    abort(404)


@app.route('/edytuj_klase/<int:klasa_id>', methods=['GET', 'POST'])
def edytuj_klase(klasa_id):
  klasa = get_klasa_or_404(klasa_id)
  form = KlasaForm(nazwa=klasa.nazwa)
  form.rok_naboru.choices = lata(-1, 10)
  form.rok_matury.choices = lata(-4, 7)

  if form.validate_on_submit():
    print(form.data)
    klasa.nazwa = form.nazwa.data
    klasa.rok_naboru = form.rok_naboru.data
    klasa.rok_matury = form.rok_matury.data
    klasa.save()
    flash("Zaktualizowano klasę: {}".format(form.nazwa.data))
    return redirect(url_for('index'))

  return render_template('edytuj_klase.html', form=form, klasa=klasa)


@app.route('/usun_klase/<int:klasa_id>', methods=['GET', 'POST'])
def usun_klase(klasa_id):
  klasa = get_klasa_or_404(klasa_id)

  if request.method == 'POST':
    klasa.delete_instance()

    return redirect(url_for('index'))
  return render_template('usun_klase.html', klasa=klasa)


@app.route('/klasy')
def klasy():
  klasy = Klasa.select()
  return render_template('klasy.html', klasy=klasy)
