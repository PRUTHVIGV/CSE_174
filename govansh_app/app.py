import os
from flask import Flask

from .config import SECRET_KEY, MAX_CONTENT_LENGTH
from .db import init_db
from .auth import auth_bp
from .core import core_bp, init_app


def create_app() -> Flask:
    here = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(here, "templates"),
        static_folder=os.path.join(here, "static"),
        static_url_path="/static",
    )
    app.secret_key = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    init_db()
    init_app()

    app.register_blueprint(auth_bp)
    app.register_blueprint(core_bp)

    return app

