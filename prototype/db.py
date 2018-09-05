from pymongo import MongoClient
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        client = MongoClient('localhost:27017')
        g.db = client['flaskr_vue_mongo']

    return g.db
