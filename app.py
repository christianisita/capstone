from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import resources
from models import db
from flask_migrate import Migrate

from config import Config

api = Api()
jwt = JWTManager()
migrate = Migrate()
blacklist = set()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist
    return app


# default endpoint for testing
api.add_resource(resources.default.DefaultEndpoint, '/')

# register endpoint
api.add_resource(resources.auth.UserRegistration, '/register')
api.add_resource(resources.auth.UserLogin, '/login')
api.add_resource(resources.patient.AddPatient, '/add_patient')
api.add_resource(resources.patient.PatientData, '/patients_data', endpoint='patients')
api.add_resource(resources.auth.AllUser, '/users')
api.add_resource(resources.patient.PatientData,'/patients_data/<id>', endpoint='patient')
api.add_resource(resources.patient.UpdatePatientData, '/patients_data/edit/<patient_id>')
api.add_resource(resources.patient.ImageDetection, '/upload/<patient_id>')






