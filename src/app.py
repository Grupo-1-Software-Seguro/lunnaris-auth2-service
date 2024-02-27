from flask import Flask, Response
from flask_cors import CORS
from routes import AuthRoutes
from dotenv import load_dotenv
from mongoengine import connect

import os


def create_app():
    load_dotenv('.env')

    connect(db=os.getenv("MONGO_DB"), host=os.getenv("MONGO_URI"))

    _app = Flask("Auth service")
    cors = CORS(_app, origins=os.getenv("FRONT_URL"))

    @_app.before_request
    def before_request():
        from flask import request
        import secrets
        request.log = {
            "log_id": secrets.token_hex(8),
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr
        }


    @_app.errorhandler(Exception)
    def handle_error(e):
        from exceptions.base_exceptions import exception_to_json
        from flask import request
        import traceback

        error, code = exception_to_json(e)
        if hasattr(request, "log"):
            stacktrace_str = traceback.format_exception(type(e), e, e.__traceback__)
            request.log["traceback"] = "".join(stacktrace_str)

        return error, code

    @_app.after_request
    def after_request(response: Response):
        import tasks
        from flask import request
        from datetime import datetime
        if hasattr(request, "log"):
            request.log["response"] = bytes(response.response[0]).decode("utf-8")
            request.log["status"] = response.status
            tasks.celery_app.send_task("logs.add_log",kwargs={
                "service": "auth",
                "timestamp": datetime.now().timestamp(),
                "log": request.log
            })

        return response

    _app.register_blueprint(AuthRoutes, url_prefix="/api/auth")
    return _app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5020, host="0.0.0.0")
