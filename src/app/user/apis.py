from flask import Blueprint, request
from core.user.services import UserService
from infrastructure.user.models import User
from app.auth.utils import decode_jwt
from app.di import injector

user_blueprint = Blueprint('user', __name__)
user_service = injector.get(UserService)

@user_blueprint.route('/profile', methods=['GET'])
def get_user_profile():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    return {
        "message": f"Welcome to {user.name}'s Profile",
        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "city": user.city,
        "about_me": user.about_me,
        "role": user.role.value
    }, 200

@user_blueprint.route('/profile/<int:user_id>', methods=['GET'])
def get_user_specific(user_id):
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)

    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    staff_or_admin = token_payload['role'] == 'STAFF' or token_payload['role'] == 'ADMIN'

    if not staff_or_admin:
        return {"error_message": "Unauthorized Access!!"}, 400

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404
    
    return {
        "user_id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "city": user.city,
        "about_me": user.about_me,
        "role": user.role.value
    }
