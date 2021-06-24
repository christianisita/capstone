from flask_jwt_extended.utils import set_access_cookies
from models.patients import Patients, Detection
from flask_restful import Resource, reqparse
import random, string
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)

def id_generator():
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return id

create_patient_parser = reqparse()
create_patient_parser.add_argument('name', required=True, help="Name cannot be blank!")
create_patient_parser.add_argument('nik', required=True, help="NIK cannot be blank!")
create_patient_parser.add_argument('age', required=True, help="Age cannot be blank")
create_patient_parser.add_argument('date_of_birth')
create_patient_parser.add_argument('address')

class AddPatient(Resource):

    @jwt_required
    def post(self):
        patient = create_patient_parser.parse_args()
        if Patients.find_by_nik(patient['nik']):
            return {
                "success": False,
                "message": "NIK already exist"
            }, HTTPStatus.OK
        new_patient = Patients(
            id = id_generator(),
            name = patient['name'],
            nik = patient['nik'],
            age = patient['age'],
            date_of_birth = patient['date_of_birth'],
            address = patient['address']
        )
    
        try:
            new_patient.save_to_db()
            return {
                "success": True,
                "message": "New patient data already created",
                "data": {
                    "id": patient['id'],
                    "name": patient['name'],
                    "nik": patient['nik'],
                    "age": patient['age'],
                    "date_of_birth": patient['date_of_birth'],
                    "address": patient['address']
                }
            }, HTTPStatus.CREATED
        
        except:
            return {
                "success": False,
                "message": "Unexpected DB Error, fail to save data to database"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

