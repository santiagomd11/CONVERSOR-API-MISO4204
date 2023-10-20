from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src import create_app, db

from views import (
    ViewRegister,
    ViewLogin
)


app = create_app('conversor')

app_context = app.app_context()
app_context.push()
db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
api.add_resource(ViewRegister, "/user-register")
api.add_resource(ViewLogin, "/login")

jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)