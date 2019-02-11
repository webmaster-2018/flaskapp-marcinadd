# -*- coding: utf-8 -*-
# quiz-orm/views.py
from datetime import datetime
from os import abort

from flask import Flask, flash, redirect, url_for, request
from flask import render_template

from forms import KlasaForm, UczenForm
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


def plec():
  return [(0, 'kobieta'), (1, 'mężczyzna')]


@app.route("/dodaj_ucznia", methods=['GET', 'POST'])
def dodaj_ucznia():
  form = UczenForm()

  form.plec.choices = plec()
  form.klasa.choices = [(klasa.id, klasa.nazwa) for klasa in Klasa.select()]

  if form.validate_on_submit():
    print(form.data)
    k = Klasa.get_by_id(form.klasa.data)
    uczen = Uczen(imie=form.imie.data, nazwisko=form.nazwisko.data, plec=form.plec.data, klasa=k.id)
    uczen.save()

    flash("Dodano ucznia: {}".format(form.imie.data))
    return redirect(url_for('index'))

  elif request.method == 'POST':
    pass
    # TODO Show errrors
    # flash_errors(form)
  return render_template('dodaj_ucznia.html', form=form)


@app.route('/uczniowie')
def uczniowie():
  uczniowie = Uczen.select()
  return render_template('uczniowie.html', uczniowie=uczniowie)


def get_uczen_or_404(uczen_id):
  try:
    uczen = Uczen.get_by_id(uczen_id)
    return uczen
  except Uczen.DoesNotExist:
    abort(404)


@app.route('/usun_ucznia/<int:uczen_id>', methods=['GET', 'POST'])
def usun_ucznia(uczen_id):
  uczen = get_uczen_or_404(uczen_id)

  if request.method == 'POST':
    uczen.delete_instance()

    return redirect(url_for('index'))
  return render_template('usun_ucznia.html', uczen=uczen)


@app.route('/edytuj_ucznia/<int:uczen_id>', methods=['GET', 'POST'])
def edytuj_ucznia(uczen_id):
  uczen = get_uczen_or_404(uczen_id)
  form = UczenForm(imie=uczen.imie, nazwisko=uczen.nazwisko)

  form.plec.choices = plec()
  form.klasa.choices = [(klasa.id, klasa.nazwa) for klasa in Klasa.select()]

  if form.validate_on_submit():
    print(form.data)
    k = Klasa.get_by_id(form.klasa.data)
    uczen.imie = form.imie.data
    uczen.nazwisko = form.nazwisko.data
    uczen.plec = form.plec.data
    uczen.klasa = k.id

    uczen.save()
    # flash("Zaktualizowano ucznia: {}".format(form.nazwa.data))
    return redirect(url_for('index'))

  return render_template('edytuj_ucznia.html', form=form, uczen=uczen)
