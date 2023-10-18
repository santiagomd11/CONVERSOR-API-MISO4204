from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models import db


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbapp.sqlite" # cambiar por posgres


app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
