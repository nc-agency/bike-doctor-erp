# setup.py für bike.doctor ERPNext-Erweiterung
# Erstellt am 2025-05-05
# Diese Datei definiert die Metadaten und Abhängigkeiten für die bike.doctor-App

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="bikedoctor",
    version="0.0.1",
    description="Bike.doctor Workshop Management System für ERPNext",
    author="bike.doctor",
    author_email="test@test.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
