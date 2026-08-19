# -*- coding: utf-8 -*-
"""Alle Blätter neu erzeugen: python3 baualle.py"""
import importlib

for nr in range(39, 100):
    try:
        modul = importlib.import_module(f'd{nr}')
    except ModuleNotFoundError:
        continue
    for pfad in modul.bau():
        print(f'{pfad.name}  {pfad.stat().st_size / 1024:.1f} KB')
