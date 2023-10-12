# import os

# class Config:
#     """Base configuration class."""
#     DEBUG = False
#     TESTING = False
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class DevelopmentConfig(Config):
#     """Development environment specific configuration."""
#     DEBUG = True
#     SQLALCHEMY_ECHO = True  # To log database queries for debugging

# class TestingConfig(Config):
#     """Testing environment specific configuration."""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite DB for testing

# class ProductionConfig(Config):
#     """Production environment specific configuration."""
#     # The base Config class already sets good defaults for production.
#     # Add any production specific configuration here.
#     pass

# # A dictionary to map an environment to its configuration class.
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }
