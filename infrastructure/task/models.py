from infrastructure.db import db
from core.task.constants import TaskPriority, TaskPurpose
from sqlalchemy import Enum

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(75), nullable=False)
    purpose = db.Column(Enum(TaskPurpose), default=TaskPurpose.GENERAL, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('tasks', lazy=True))