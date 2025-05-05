# -*- coding: utf-8 -*-
# setup.py für bike.doctor App
#
# Erstellt: 04.05.2025
# Änderungen:
# - Initiale Erstellung der setup.py für die bike.doctor-App
# 
# Diese Datei definiert die Installationsparameter für die bike.doctor-App.

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="bikedoctor",
    version="0.0.1",
    description="ERPNext-Anwendung für die Fahrradwerkstatt bike.doctor",
    author="bike.doctor Team",
    author_email="info@bike.doctor",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
