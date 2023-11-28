from flask import Blueprint, request
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError, validate
from core.auth.services import AuthService
from core.user.constants import UserRole
from app.di import injector

auth_blueprint = Blueprint('auth', __name__)
auth_service = injector.get(AuthService)

class UserRegistrationSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    name = fields.String(required=True)
    city = fields.String(required=True)
    about_me = fields.String(required=True)
    role = fields.Enum(UserRole, required=True)

@auth_blueprint.route('/registration', methods=['POST'])
def register_user():
    data = request.get_json()
    schema = UserRegistrationSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400

    result = auth_service.register(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        name=data['name'],
        city=data['city'],
        about_me=data['about_me'],
        role=data['role']
    )
    
    return result

class UserLoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    password = fields.String(required=True, validate=validate.Length(min=8))

@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    schema = UserLoginSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400

    result = auth_service.login(
        username=data['username'],
        password=data['password']
    )

    if not result:
        return {"error_message": "Invalid Username/Password"}, 401

    return result