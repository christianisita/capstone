from flask_jwt_extended.utils import set_access_cookies
from models.patients import Patients, Detection
from flask_restful import Resource, reqparse
import random, string
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)

def id_generator():
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return id

create_patient_parser = reqparse.RequestParser()
create_patient_parser.add_argument('name', required=True, help="Name cannot be blank!")
create_patient_parser.add_argument('patient_number', required=True, help="Patient Number cannot be blank!")
create_patient_parser.add_argument('age', required=True, help="Age cannot be blank")
create_patient_parser.add_argument('date_of_birth')
create_patient_parser.add_argument('address')

class AddPatient(Resource):

    @jwt_required()
    def post(self):
        patient = create_patient_parser.parse_args()
        if Patients.find_by_patient_number(patient['patient_number']):
            return {
                "success": False,
                "message": "Patient Number already exist"
            }, HTTPStatus.OK
        new_patient = Patients(
            id = id_generator(),
            name = patient['name'],
            patient_number = patient['patient_number'],
            age = patient['age'],
            date_of_birth = patient['date_of_birth'],
            address = patient['address']
        )
    
        try:
            new_patient.save_to_db()
            current_patient = Patients.find_by_patient_number(patient['patient_number'])
            return {
                "success": True,
                "message": "New patient data already created",
                "data": {
                    "id": current_patient.id,
                    "name": current_patient.name,
                    "patient_number": current_patient.patient_number,
                    "age": current_patient.age,
                    "date_of_birth": current_patient.date_of_birth,
                    "address": current_patient.address
                }
            }, HTTPStatus.CREATED
        
        except:
            return {
                "success": False,
                "message": "Unexpected DB Error, fail to save data to database"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

class PatientData(Resource):
    
    @jwt_required()
    def get(self):
        try:
            all_data = Patients.get_all_patient_data()
            def to_dict(x):
                return {
                    "id": x.id,
                    "name": x.name,
                    "patient_number": x.patient_number,
                    "age": x.patient_number,
                    "date_of_birth": x.date_of_birth,
                    "address": x.address
                }
            return {
                "succes": True,
                "message": "Success get all patient data",
                "data": {
                    "users": list(map(lambda x: to_dict(x), all_data))
                }
            }, HTTPStatus.OK
        except:
            return {
                "success": False,
                "message": "Error getting data"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

