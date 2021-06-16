import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '.env')
load_dotenv(env_path)

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'rahasia-dong'
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    JWT_BLACKLIST_ENABLED = os.environ.get("JWT_BLACKLIST_ENABLED")
    JWT_BLACKLIST_TOKEN_CHECKS = os.environ.get("JWT_BLACKLIST_TOKEN_CHECKS")

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class StagingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

env_config = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig
}