from flask import Flask
import os
from routes import AuthRoutes
from dotenv import load_dotenv
from mongoengine import connect
import exceptions
from provider import ServiceProvider
from utils import exception_to_json


load_dotenv('.env')
connect(db=os.getenv("MONGO_DB"), host=os.getenv("MONGO_URI"))


app = Flask("Auth service")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS").lower() == "true"
app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL").lower() == "true"

provider = ServiceProvider()
provider.init_app(app)

"""
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return exception_to_json(exceptions.NotAuthorized())


@jwt.token_verification_failed_loader
def verification_failed():
    raise exceptions.InvalidToken
"""

@app.errorhandler(Exception)
def handle_error(e):
    return exception_to_json(e)

app.register_blueprint(AuthRoutes, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(debug=True, port=5020)
