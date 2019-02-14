# -*- coding: utf-8 -*-
# quiz-orm/views.py
from datetime import datetime

from flask import Flask, flash, redirect, url_for, request
from flask import render_template
from playhouse.flask_utils import get_object_or_404

from forms import KlasaForm, UczenForm
from modele import *

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


lista_plec = [(0, 'kobieta'), (1, 'mężczyzna')]


def lata(a, b):
  rok = datetime.now().year
  lata_lista = []
  for i in range(a, b):
    lata_lista.append((rok - i, rok - i))

  return lata_lista


@app.route('/')
def index():
    """Strona główna"""
    return render_template('index.html')


#################################
# Obsługa klas
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
    return redirect(url_for('klasy'))

  elif request.method == 'POST':
    pass
    # TODO Show errrors
    # flash_errors(form)
  return render_template('dodaj_klase.html', form=form)


@app.route('/edytuj_klase/<int:klasa_id>', methods=['GET', 'POST'])
def edytuj_klase(klasa_id):
  klasa = get_object_or_404(Klasa, Klasa.id == klasa_id)
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
  klasa = get_object_or_404(Klasa, Klasa.id == klasa_id)

  if request.method == 'POST':
    klasa.delete_instance()

    return redirect(url_for('index'))
  return render_template('usun_klase.html', klasa=klasa)


@app.route('/klasy')
def klasy():
  klasy_lista = Klasa.select()
  return render_template('klasy.html', klasy=klasy_lista)


#################################
# Obsługa uczniów

@app.route("/dodaj_ucznia", methods=['GET', 'POST'])
def dodaj_ucznia():
  form = UczenForm()

  form.plec.choices = lista_plec
  form.klasa.choices = [(klasa.id, klasa.nazwa) for klasa in Klasa.select()]

  if form.validate_on_submit():
    print(form.data)
    k = Klasa.get_by_id(form.klasa.data)
    uczen = Uczen(imie=form.imie.data, nazwisko=form.nazwisko.data,
                  plec=form.plec.data, klasa=k.id)
    uczen.save()

    flash("Dodano ucznia: {}".format(form.imie.data))
    return redirect(url_for('uczniowie'))

  elif request.method == 'POST':
    pass
    # TODO Show errrors
    # flash_errors(form)
  return render_template('dodaj_ucznia.html', form=form)


@app.route('/uczniowie')
def uczniowie():
  uczniowie_lista = Uczen.select()
  return render_template('uczniowie.html', uczniowie=uczniowie_lista)


@app.route('/usun_ucznia/<int:uczen_id>', methods=['GET', 'POST'])
def usun_ucznia(uczen_id):
  uczen = get_object_or_404(Uczen, Uczen.id == uczen_id)

  if request.method == 'POST':
    uczen.delete_instance()

    return redirect(url_for('index'))
  return render_template('usun_ucznia.html', uczen=uczen)


@app.route('/edytuj_ucznia/<int:uczen_id>', methods=['GET', 'POST'])
def edytuj_ucznia(uczen_id):
  uczen = get_object_or_404(Uczen, Uczen.id == uczen_id)
  form = UczenForm(imie=uczen.imie, nazwisko=uczen.nazwisko)

  form.plec.choices = lista_plec
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
