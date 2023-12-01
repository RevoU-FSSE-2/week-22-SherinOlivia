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

    def create(self, user_id: int, title: str, description: str, purpose: str, priority: str, status: str, due_date: datetime) -> TaskDomain:
        task = self.task_accessor.create(user_id=user_id, title=title, description=description, purpose=purpose, priority=priority, status=status, due_date=due_date)
        user = self.user_accessor.get_by_id(user_id)

        if len(description) > 150:
            return {"error_message": "Description Can't be longer than 150 characters"}, 400
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "purpose": task.purpose.value,
            "priority": task.priority.value,
            "status": task.status.value,
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
            return None
        return tasks
    
    def edit(self, task_id: int, user_id: int, title: str, description: str, purpose: str, priority: str, due_date: datetime):
        task = self.task_accessor.get_by_id(task_id)
        if not task:
            return {"error message": "Task not Found"}, 404
        edited_task = self.task_accessor.edit(task_id, user_id, title=title, description=description, purpose=purpose, priority=priority, due_date=due_date)
        user = self.user_accessor.get_by_id(user_id)    

        if len(description) > 150:
            return {"error_message": "Description Can't be longer than 150 characters"}, 400
        
        return {
            "id": edited_task.id,
            "user_id": user.id,
            "name": user.name,
            "title": edited_task.title,
            "description": edited_task.description,
            "purpose": edited_task.purpose.value,
            "priority": edited_task.priority.value,
            "due_date": edited_task.due_date
        }, 200
    
    def update(self, task_id: int, user_id: int, status: str):
        updated_task = self.task_accessor.update(task_id, user_id, status)

        if isinstance(updated_task, dict) and "error_message" in updated_task:
            
            return {"error_message": updated_task["error_message"]}, 400

        user = self.user_accessor.get_by_id(user_id)
        staff_or_admin = user.role.value == 'STAFF' or user.role.value == 'ADMIN'

        if staff_or_admin:
            return {"message": f"Task successfully updated by {user.role}"}, 200

        return {"message": f"Task successfully updated by {user.name}"}, 200


    def delete(self, task_id: int, user_id: int):
        task = self.task_accessor.get_by_id(task_id)
        if not task:
            return {"error message": "Task not Found"}, 404
        user = self.user_accessor.get_by_id(user_id)
        staff_or_admin = user.role.value == 'STAFF' or user.role.value == 'ADMIN'
        if staff_or_admin:
            task = self.task_accessor.delete(task_id, user_id)
            return {"message": f"Task successfully deleted by {user.role}"}, 200
        
        if task.user_id != user.id:
            return {"error message": f"Task doesn't belong to {user.name}!"}, 400
        
        task = self.task_accessor.delete(task_id=task_id, user_id=user_id)
        
        return {"message": f"Task successfully deleted by {user.name}"}, 200