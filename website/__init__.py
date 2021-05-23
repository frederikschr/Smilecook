import os
from flask import Flask, session
from datetime import timedelta

URL = os.environ["SMILE_BASE_URL"]

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "adadwad"
    app.secret_key = "awdwadwadawd"
    app.permanent_session_lifetime = timedelta(days=3)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
