from core.common.utils import SoftDeleteMixin
from infrastructure.db import db
from core.task.constants import TaskPriority, TaskPurpose, TaskStatus
from sqlalchemy import Enum

class Task(db.Model, SoftDeleteMixin):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(75), nullable=False)
    purpose = db.Column(Enum(TaskPurpose), default=TaskPurpose.GENERAL, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(Enum(TaskPriority), default=TaskPriority.LOW, nullable=False)
    status = db.Column(Enum(TaskStatus), default=TaskStatus.ONGOING, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('tasks', lazy=True))