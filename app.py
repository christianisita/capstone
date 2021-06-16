from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import resources
from models import db
from flask_migrate import Migrate

from config import env_config

api = Api()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(env_config[config_name])
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    return app


# default endpoint for testing
api.add_resource(resources.default.DefaultEndpoint, '/')

# register endpoint
api.add_resource(resources.auth.UserRegistration, '/register')
api.add_resource(resources.auth.UserLogin, '/login')







