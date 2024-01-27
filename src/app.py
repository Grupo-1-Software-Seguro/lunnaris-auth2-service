from flask import Flask
import os
from routes import AuthRoutes
from dotenv import load_dotenv
from mongoengine import connect
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
import exceptions
from utils import exception_to_json


load_dotenv('.env')
connect(db=os.getenv("MONGO_DB"), host=os.getenv("MONGO_URI"))


app = Flask("Auth service")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

app.register_blueprint(AuthRoutes, url_prefix="/api/auth")
jwt = JWTManager(app)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return exception_to_json(exceptions.NotAuthorized())


@jwt.token_verification_failed_loader
def verification_failed():
    raise exceptions.InvalidToken


@app.errorhandler(Exception)
def handle_error(e):
    return exception_to_json(e)



if __name__ == "__main__":
    app.run(debug=True, port=5020)
