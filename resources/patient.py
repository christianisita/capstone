from flask_jwt_extended.utils import set_access_cookies
from sqlalchemy.sql.elements import Null
from models.patients import Patients, Detection
from flask_restful import Resource, reqparse
from flask import request
import random, string
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from flask import current_app as app
from werkzeug.utils import secure_filename
import os
from tensorflow import keras
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from resources.preprocessing import Preprocessing
from datetime import datetime

#model = keras.models.load_model("./detection-model/preprocessed-01.hdf5")
json_file = open('./detection-model/model_num.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("./detection-model/preprocessed-01.hdf5")

def id_generator():
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return id

create_patient_parser = reqparse.RequestParser()
create_patient_parser.add_argument('name', required=True, help="Name cannot be blank!")
create_patient_parser.add_argument('patient_number', required=True, help="Patient Number cannot be blank!")
create_patient_parser.add_argument('age', required=True, help="Age cannot be blank")
create_patient_parser.add_argument('date_of_birth')
create_patient_parser.add_argument('gender')
create_patient_parser.add_argument('address')

class AddPatient(Resource):
    @jwt_required
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
            gender = patient['gender'],
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
                    "gender": current_patient.gender,
                    "address": current_patient.address
                }
            }, HTTPStatus.CREATED
        
        except:
            return {
                "success": False,
                "message": "Unexpected DB Error, fail to save data to database"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

class PatientData(Resource):
    @jwt_required
    def get(self, id=None):
        if id==None:
            try:
                all_data = Patients.get_all_patient_data()
                def to_dict(x):
                    return {
                        "id": x.id,
                        "name": x.name,
                        "patient_number": x.patient_number,
                        "age": x.patient_number,
                        "date_of_birth": x.date_of_birth,
                        "gender": x.gender,
                        "address": x.address
                    }
                return {
                    "success": True,
                    "message": "Success get all patient data",
                    "data": {
                        "patients": list(map(lambda x: to_dict(x), all_data))
                    }
                }, HTTPStatus.OK
            except:
                return {
                    "success": False,
                    "message": "Error getting data"
                }, HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            try:
                patient = Patients.find_by_patient_id(id)
                return {
                    "success": True,
                    "message": "Success get patient data",
                    "data": {
                        "id": patient.id,
                        "name": patient.name,
                        "patient_number": patient.patient_number,
                        "age": patient.age,
                        "date_of_birth": patient.date_of_birth,
                        "gender": patient.gender,
                        "address": patient.address
                    }
                }, HTTPStatus.OK
            except:
                return {
                    "success": False,
                    "message": "Error getting data"
                }, HTTPStatus.INTERNAL_SERVER_ERROR

update_patient_parser = reqparse.RequestParser()
update_patient_parser.add_argument('name')
update_patient_parser.add_argument('patient_number')
update_patient_parser.add_argument('date_of_birth')
update_patient_parser.add_argument('age')
update_patient_parser.add_argument('gender')
update_patient_parser.add_argument('address')

class UpdatePatientData(Resource):
    @jwt_required
    def put(self, patient_id):
        if not Patients.find_by_patient_id(patient_id):
            return {
                "success": False,
                "message": "Patient data is not exist."
            }, HTTPStatus.NOT_FOUND
        patient = Patients.find_by_patient_id(patient_id)
        updated = update_patient_parser.parse_args()
        if updated['name']:
            patient.name = updated['name']
        if updated['patient_number']:
            patient.patient_number = updated['patient_number']
        if updated['date_of_birth']:
            patient.date_of_birth = updated['date_of_birth']
        if updated['age']:
            patient.age = updated['age']
        if updated['gender']:
            patient.gender = updated['gender']
        if updated['address']:
            patient.address = updated['address']
        
        try:
            patient.save_to_db()
            current_patient = Patients.find_by_patient_id(patient_id)
            return {
                "succes": True,
                "message": "Success edit patient data",
                "data": {
                    "id" : current_patient.id,
                    "name" : current_patient.name,
                    "patient_number": current_patient.patient_number,
                    "date_of_birth": current_patient.date_of_birth,
                    "age": current_patient.age,
                    "gender": current_patient.gender,
                    "address": current_patient.address
                }
            }, HTTPStatus.OK
        except:
            return {
                "success": False,
                "message": "failed edit patient data"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

class ImageDetection(Resource):
    @jwt_required
    def post(self, patient_id):
        UPLOAD_FILE_DESTINATION = app.config['UPLOAD_FOLDER']
        if not Patients.find_by_patient_id(patient_id):
            return {
                "success": False,
                "message": "Patient doesn't exist!"
            }, HTTPStatus.NOT_FOUND
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            extension = os.path.splitext(filename)[1]
            name = patient_id + '-' + str(datetime.now())
            filepath = os.path.join(UPLOAD_FILE_DESTINATION, str(name+extension))
            file.save(filepath)
            img_path = Preprocessing.preprocessing(filepath)
            img = keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
            x = keras.preprocessing.image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            img_preprocessed = preprocess_input(x)
            prediction = model.predict(img_preprocessed)
            predicted = np.argmax(prediction, axis=1)[0]
            predicted = str(predicted)

            uploaded_files = Detection(
                id = id_generator(),
                patient_id = patient_id,
                file_path = filepath,
                detection = predicted
            )

            uploaded_files.save_to_db()
            patient_data = Patients.find_by_patient_id(patient_id)
            detection_data = Detection.find_by_id(uploaded_files.id)
            return {
                "success": True,
                "message": "success upload file",
                "data": {
                    "detection_id": detection_data.id,
                    "image_path": detection_data.file_path,
                    "patient_id": patient_data.id,
                    "patient_name": patient_data.name,
                    "patient_number": patient_data.patient_number,
                    "detection": detection_data.detection
                }
            }
        except Exception as e:
            raise e
            # return {
            #     "success": False,
            #     "message": "error upload file"
            # }

class SinglePatientHistory(Resource):
    @jwt_required
    def get(self, patient_id):
        if not Patients.find_by_patient_id(patient_id):
            return {
                "success": False,
                "message": "Patient doesn't exist!"
            }, HTTPStatus.NOT_FOUND
        try:
            patient_data = Patients.find_by_patient_id(patient_id)
            detection_histories = Detection.single_patient_histories(patient_id)

            def dict_histories(x):
                return {
                        "date": x.created_at.__str__(),
                        "detection" : x.detection,
                        "file_path" : x.file_path
                }
            return {
                "success": True, 
                "message": "Success getting detection data!",
                "data": {
                    "patient_id": patient_data.id,
                    "patient_number": patient_data.patient_number,
                    "patinet_name": patient_data.name,
                    "age": patient_data.age, 
                    "address": patient_data.address,
                    "gender": patient_data.gender,
                    "detection_data": list(map(lambda x: dict_histories(x), detection_histories))
                }
            }, HTTPStatus.OK
        except:
            return {
                "success": False,
                "message": "Error geting data"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

class AllPatientsHistoriesLatest(Resource):
    @jwt_required
    def get(self):
        
        all_detection_data = Detection.latest_all()
        def to_dict(x):
            return {
                "patient_id": x.id,
                "patient_number": x.patient_number,
                "patient_name": x.name,
                "patient_age": x.age,
                "patient_address": x.address,
                "detection": x.detection,
                "detection_date": x.detection_date.__str__(),
                "file_path": x.file_path
            }
        return {
            "data": list(map(lambda x: to_dict(x),all_detection_data))
        }
        


