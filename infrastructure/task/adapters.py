from core.task.models import TaskDomain
from core.common.utils import ObjectMapperUtil
from core.task.ports import ITaskAccessor
from infrastructure.db import db
from infrastructure.task.models import Task
from infrastructure.user.models import User

from infrastructure.task.constants import DUE_DATE_FORMAT
from datetime import datetime

class TaskAccessor(ITaskAccessor):

    def create(self, user_id: int, title:str, description: str, purpose: str, priority: str, due_date: datetime):
        user = User.query.get(user_id)
        new_task = Task(user_id=user.id, title=title, description=description, purpose=purpose, priority=priority, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()

        return ObjectMapperUtil.map(new_task, TaskDomain)

    def get_by_user_id(self, user_id: int):
        user = User.query.get(user_id)
        tasks = Task.query.filter_by(user_id=user.id).all()

        return [ObjectMapperUtil.map(task, TaskDomain) for task in tasks]
    
    def get_by_id(self, task_id: int):
        task = Task.query.get(task_id)
        return ObjectMapperUtil.map(task, TaskDomain)
    
    def update(self, task_id: int, user_id: int, title: str, description: str, purpose: str, priority: str, due_date: datetime):
        user = User.query.get(user_id)
        task = Task.query.get(task_id)
        
        if not task:
            return {"error message": "Task not Found"}, 404

        # Update data
        task.title = title
        task.description = description
        task.purpose = purpose
        task.priority = priority
        task.due_date = due_date

        db.session.commit()

        return ObjectMapperUtil.map(task, TaskDomain)