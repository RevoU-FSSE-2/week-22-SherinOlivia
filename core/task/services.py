import os, jwt
from injector import inject
from core.task.models import TaskDomain
from core.task.ports import ITaskAccessor
from core.user.ports import IUserAccessor
from datetime import datetime, timedelta

class TaskService():

    @inject
    def __init__(self, task_accessor: ITaskAccessor, user_accessor: IUserAccessor) -> None:
        self.task_accessor = task_accessor
        self.user_accessor = user_accessor

    def create(self, user_id: int, title: str, description: str, purpose: str, priority: str, due_date: datetime) -> TaskDomain:
        task = self.task_accessor.create(user_id=user_id, title=title, description=description, purpose=purpose, priority=priority, due_date=due_date)
        user = self.user_accessor.get_by_id(user_id)

        if len(description) > 150:
            return {"error_message": "Description Can't be longer than 150 characters"}, 400
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "purpose": task.purpose.value,
            "priority": task.priority.value,
            "due_date": task.due_date,
            'user_id': user.id,
            "username": user.username
        }, 200
    
    def get_by_user_id(self, user_id: int):
        tasks = self.task_accessor.get_by_user_id(user_id)
        
        if not tasks:
            return {"error message": "Task not Found"}, 404

        return tasks
    
    def get_by_id(self, task_id: int):
        tasks = self.task_accessor.get_by_id(task_id)
        
        if not tasks:
            return {"error message": "Task not Found"}, 404

        return tasks
    
    def update(self, task_id: int, user_id: int, title: str, description: str, purpose: str, priority: str, due_date: datetime):
        task = self.task_accessor.get_by_id(task_id)
        if not task:
            return {"error message": "Task not Found"}, 404
        updated_task = self.task_accessor.update(task_id, user_id, title=title, description=description, purpose=purpose, priority=priority, due_date=due_date)
        user = self.user_accessor.get_by_id(user_id)    

        if len(description) > 150:
            return {"error_message": "Description Can't be longer than 150 characters"}, 400
        
        return {
            "id": updated_task.id,
            "user_id": user.id,
            "name": user.name,
            "title": updated_task.title,
            "description": updated_task.description,
            "purpose": updated_task.purpose.value,
            "priority": updated_task.priority.value,
            "due_date": updated_task.due_date
        }, 200