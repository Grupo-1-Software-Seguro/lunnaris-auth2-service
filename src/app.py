from flask import Flask
import os

from flask_cors import CORS

from routes import AuthRoutes
from dotenv import load_dotenv
from mongoengine import connect


def create_app():
    load_dotenv('.env')

    connect(db=os.getenv("MONGO_DB"), host=os.getenv("MONGO_URI"))

    _app = Flask("Auth service")
    cors = CORS(_app, origins=os.getenv("FRONT_URL"))

    @_app.errorhandler(Exception)
    def handle_error(e):
        from exceptions.base_exceptions import exception_to_json
        from utils.logger import log_to_file
        log_to_file(f"{type(e)}: {e}")
        return exception_to_json(e)

    _app.register_blueprint(AuthRoutes, url_prefix="/api/auth")
    return _app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5020)
