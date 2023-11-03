import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    # Create a log directory if it does not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up logging
    file_handler = RotatingFileHandler('logs/myapp.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))

    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Log that the logger has been configured
    app.logger.info('Logging setup completed')
