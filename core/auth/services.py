import os, jwt
from injector import inject
from core.auth.ports import IHashingAccessor
from core.user.ports import IUserAccessor
from core.user.constants import UserRole
from core.user.models import UserDomain
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AuthService():

    @inject
    def __init__(self, user_accessor: IUserAccessor, hashing_accessor: IHashingAccessor) -> None:
        self.user_accessor = user_accessor
        self.hashing_accessor = hashing_accessor

    def register(self, username: str, password: str, email: str, name: str, city: str, about_me: str, role: UserRole) -> UserDomain:
        hashed_password = self.hashing_accessor.generate(password)
        existing_user = self.user_accessor.get_by_username(username=username)

        if existing_user.username is not None:
            return {"error message": "username already taken" }, 400

        user = self.user_accessor.create(
            username=username,
            hashed_password=hashed_password,
            email=email,
            name=name,
            city=city,
            about_me=about_me,
            role=role
        )

        return {
            'user_id': user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "city": user.city,
            "about_me": user.about_me,
            "role": user.role.value
        }, 200

    def login(self, username: str, password: str):
        valid_user = self.user_accessor.get_by_username(username=username)
        if not valid_user:
            return {"error_message": "Invalid Username/Password"}, 401

        valid_password = self.hashing_accessor.check_hash(valid_user.password, password)
        if not valid_password:
            return {"error_message": "Invalid Username/Password"}, 401
        
        token_payload = {
            'user_id': valid_user.id, 
            'username': valid_user.username, 
            'role': valid_user.role.value,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        secret_key = os.getenv("SECRET_KEY")
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')

        return {
            "message": f"Welcome {valid_user.name}!",
            'id': valid_user.id,
            'username': valid_user.username,
            'token': token
            }, 200


        