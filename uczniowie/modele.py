#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  modele.py

from peewee import *

baza_plik = 'baza.db'
baza = SqliteDatabase(baza_plik)  # instancja bazy


### MODELE
class BazaModel(Model):
    class Meta:
        database = baza


class Klasa(BazaModel):
  nazwa = CharField(null=False)
  rok_naboru = CharField(null=False)
  rok_matury = CharField(null=False)


class Uczen(BazaModel):
  imie = CharField(null=False)
  nazwisko = CharField(null=False)
  klasa = ForeignKeyField(Klasa, related_name='klasy')
  data_ur = DateField
