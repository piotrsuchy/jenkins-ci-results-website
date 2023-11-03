from app import create_app
from app import logging_config

app = create_app()
logging_config.configure_logging(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)