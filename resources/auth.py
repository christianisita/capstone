from flask_jwt_extended.utils import set_access_cookies
from models.users import UserModel, RevokedTokenModel
from flask_restful import Resource, reqparse
import random, string
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
# from app import api

def id_generator():
    id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return id

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('name', required=True, help="Name cannot be blank!")
registration_parser.add_argument('email', required=True, help="Email cannot be blank!")
registration_parser.add_argument('username', required=True, help="Username cannot be blank")
registration_parser.add_argument('password', required=True, help="Password cannot be blank!")
registration_parser.add_argument('role', required=True, help="Role cannot be blank")

class UserRegistration(Resource):
    def post(self):
        data = registration_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {
                "success": False, 
                "message": "Username: {} already exist!".format(data['username'])
            }, HTTPStatus.BAD_REQUEST

        if UserModel.find_by_email(data['email']):
            return {
                "success": False,
                "message": "Email: {} already exist!".format(data['email'])
            }, HTTPStatus.BAD_REQUEST

        new_user = UserModel(
            id = id_generator(),
            name = data['name'],
            email = data['email'],
            username = data['username'],
            password = UserModel.generate_hash(data['password']),
            role = data['role']
        )
        try :
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            #print(str(access_token))
            refresh_token = create_refresh_token(identity = data['username'])
            #print(str(refresh_token))
            return {
                "success": True,
                "message": "User already created",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "name": data['name'],
                    "email": data['email'],
                    "username": data['username'],
                    "role": data['role']
                }
            }, HTTPStatus.CREATED
        except:
            return {
                "success": False,
                "message": "Something went wrong, please try again!"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True)
login_parser.add_argument('password',required=True)

class UserLogin(Resource):
    def post(self):
        data = login_parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {
                "success": False,
                "message": "Username {} not found".format(data['username'])
            }, HTTPStatus.NOT_FOUND
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                "success": True,
                "message": "You are successfully logged in",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_id": current_user.id,
                    "name": current_user.name,
                    "username": current_user.username,
                    "email": current_user.email,
                    "role": current_user.role
                }
            }, HTTPStatus.OK
        else:
            return {
                "success": False,
                "message": "Invalid password"
            }, HTTPStatus.OK

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {
            "access_token": access_token
        }
