from flask import Flask
from .database.init_db import initialize_database
from .blueprints.web_routes import web
from .blueprints.api_routes import api
from .progress_manager import ProgressManager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    app.progress_manager = ProgressManager()
    # register blueprints
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')

    initialize_database()

    return app