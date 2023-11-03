import os
from flask import Flask
from .database.init_db import initialize_database
from .blueprints.web_routes import web
from .blueprints.api_routes import api
from .progress_manager import ProgressManager
from .setup_teardown_duration import SetupDuration, TeardownDuration


def create_app():
    app = Flask(__name__)
    
    env = os.environ.get('FLASK_ENV', 'default') # if not set - default to development
    # app.config.from_object(config[env])
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    app.progress_manager = ProgressManager()
    app.setup_duration = SetupDuration()
    app.teardown_duration = TeardownDuration()
    # register blueprints
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix='/api')

    initialize_database()

    return app
    