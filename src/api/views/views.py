from flask import request
from flask import jsonify
from flask import current_app
from flask_restful import Resource
import hashlib
from flask import send_file
from pathlib import Path
from datetime import datetime
from moviepy.editor import *
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os

from models import (
    db,
    User,
    UserSchema,
    Task,
    TaskSchema,
    FileExtensions,
    ConversionFile
)

user_schema = UserSchema()
task_schema = TaskSchema()


from celery import Celery

celery_app = Celery(
    'conversor',
    broker='pyamqp://guest@localhost//',
    backend='rpc://',
)

celery_app.conf.update(
    result_expires=3600,
)

class ViewRegister(Resource):
    def post(self):
        email_request = request.json["email"]
        user_request = request.json["user"]

        exist_email = User.query.filter(
            User.email == email_request
        ).first()

        exist_user = User.query.filter(
            User.user == user_request
        ).first()

        if exist_email is None and exist_user is None:
            password_encrypt = hashlib.sha3_512(
                request.json["password"].encode("utf-8")
            ).hexdigest()
            new_user = User(
                user = user_request,
                email = email_request,
                password = password_encrypt,
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User create successful"}, 201
        else:
            return {"message": "User or email already exist"}, 409
        

class ViewLogin(Resource):
    def post(self):
        password_encrypt = hashlib.sha3_512(
            request.json["password"].encode("utf-8")
        ).hexdigest()

        user_email_request = request.json["user"]

        query_email = User.query.filter(
            User.email == user_email_request,
            User.password == password_encrypt,
        ).first()

        query_user = User.query.filter(
            User.user == user_email_request,
            User.password == password_encrypt,
        ).first()

        if query_email != None:
            token_access = create_access_token(identity = query_email.id)
        elif query_user != None:
            token_access = create_access_token(identity = query_user.id)
        else:
            return {"message": "User not found"}, 404

        return {
            "message": "Login success",
            "token": token_access,
        }, 200
    
class ViewTask(Resource):
    @jwt_required()
    def get(self, id_task):
        task = Task.query.get_or_404(id_task)
        return task_schema.dump(Task.query.get_or_404(task.id))
    
    @jwt_required()
    def delete(self, id_task):
        try:
            task = Task.query.get_or_404(id_task)
            db.session.delete(task)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify(error=str(e)), 500


class ViewTasks(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity() 
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        return task_schema.dump(tasks, many=True)
    
import multiprocessing

@celery_app.task
def convert_video_async(filename, target_format, current_user_id):
    video = VideoFileClip(filename)
    original_extension = filename.split('.')[1]
    converted_file_name = filename.split('.')[0] + '_converted' + '.' + target_format.lower()
    desktop_path = Path.home()

    converted_file_path = desktop_path / converted_file_name

    video.write_videofile(str(converted_file_path))
    
    timestamp = datetime.now()
    file_status = "processed"
    conversion_task = ConversionFile(file_name=converted_file_name, timestamp=timestamp, status=file_status)
    db.session.add(conversion_task)
    db.session.commit()
    
    task = Task(original_file_name=filename, original_file_extension=FileExtensions(original_extension.lower()),
                converted_file_extension=FileExtensions(target_format.lower()), is_available=True,
                original_file_url=filename, converted_file_url=converted_file_name,
                user_id=current_user_id, conversion_file=conversion_task)
    db.session.add(task)
    db.session.commit()
    
class ViewUploadAndConvert(Resource):
    @jwt_required()
    def get(self):
        auth_token = request.headers.get('Authorization')
        current_user_id = get_jwt_identity() 
        if not auth_token:
            return {'message': 'Token de autenticación inválido'}, 401 
        
        file = request.files['file']
        target_format = request.form['target_format']
        
        if target_format.lower() not in [e.value for e in FileExtensions]:
            return {'message': 'Formato de destino no admitido'}, 400 
        
        
        filename = secure_filename(file.filename)
        file.save(filename)

        p = multiprocessing.Process(target=convert_video_async, args=(filename, target_format, current_user_id))
        p.start()

        return {'message': 'La conversión se ha iniciado de manera asíncrona.'}, 200


class ViewDownload(Resource):
    @jwt_required()
    def get(self, file_name):
        desktop_path = Path.home()
        converted_file_path = desktop_path / file_name
        try:
            return send_file(converted_file_path, as_attachment=True)
        except Exception as e:
            return {'message': f'Error al obtener el archivo: {e}'}, 500