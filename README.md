Plus technique, plus destiné a ceux qui vont tester le projet

Au format markdown. Ce fichier explique comment lancer le projet. Il indique également les
éventuelles contraintes sur la version de Python à utiliser pour exécuter le projet.

Lancer le projet : 
```bash
# DANS LE ROOT DU PROJET
cd src

python -m venv .venv
.venv/bin/pip install -r ./requirements.txt
.venv/bin/python ./main.py
```