from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    
    
class FileExtensions(Enum):
    MP4 = 'mp4'
    WEBM = 'webm'
    AVI = 'avi'
    MPEG = 'mpeg'
    WMV = 'wmw'    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_file_name = db.Column(db.String(2000))
    original_file_extension = db.Column(db.Enum(FileExtensions))
    converted_file_extension  = db.Column(db.Enum(FileExtensions))
    is_available =  db.Column(db.Boolean)
    original_file_url = db.Column(db.String(2000))
    converted_file_url = db.Column(db.String(2000))
    
class ConversionFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))
        
    

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    id = fields.String()

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
    
    id = fields.String()