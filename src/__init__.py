from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://trayectosuser:mystrongpassword@db:5432/mydb'
    db.init_app(app)
    return app
