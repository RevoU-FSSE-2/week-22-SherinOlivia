from infrastructure.db import db
from core.user.constants import UserRole
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(75), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(75), nullable=False)
    city = db.Column(db.String(75), nullable=False)
    about_me = db.Column(db.String(150), nullable=False)
    role = db.Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)