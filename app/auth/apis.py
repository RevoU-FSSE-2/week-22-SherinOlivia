from flask import Blueprint, request
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError, validate
from app.auth.utils import decode_jwt
from app.common.utils import sanitize_input
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
    role = fields.Enum(UserRole, missing=UserRole.CLIENT)

@auth_blueprint.route('/registration', methods=['POST'])
@sanitize_input
def register_user():
    data = request.sanitized_data
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
@sanitize_input
def login_user():
    data = request.sanitized_data
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

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401
    return {"message": "Logout successful. See you next time!"}, 200