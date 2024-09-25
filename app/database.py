import mysql.connector
from flask import current_app, g
import os

def init_db(app):
    app.config['DB_CONFIG'] = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'port': os.getenv('DB_PORT')
    }

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**current_app.config['DB_CONFIG'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
