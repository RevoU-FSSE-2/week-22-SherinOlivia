from flask import Blueprint, request
from core.task.constants import TaskPurpose, TaskPriority, TaskStatus
from core.task.services import TaskService
from core.user.services import UserService
from infrastructure.task.constants import DUE_DATE_FORMAT
from app.auth.utils import decode_jwt
from app.di import injector
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

from infrastructure.task.models import Task

task_blueprint = Blueprint('task', __name__)
task_service = injector.get(TaskService)
user_service = injector.get(UserService)

class CreateTaskSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    purpose = fields.Enum(TaskPurpose, required=True)
    priority = fields.Enum(TaskPriority, required=True)
    due_date = fields.DateTime(format=DUE_DATE_FORMAT, required=True)
    status = fields.Enum(TaskStatus, missing=TaskStatus.ONGOING)

@task_blueprint.route('/create', methods=['POST'])
def create_task():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    data = request.get_json()
    schema = CreateTaskSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400

    if len(data['description']) > 150:
        return {"error_message": "Description Can't be longer than 150 characters"}, 400

    result = task_service.create(
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        purpose=data['purpose'],
        status=data['status'],
        priority=data['priority'],
        due_date = data['due_date']
    )

    return result

@task_blueprint.route('/list', methods=['GET'])
def get_task_list():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)
    staff_or_admin = token_payload['role'] == 'STAFF' or token_payload['role'] == 'ADMIN'

    if staff_or_admin:
        tasks = Task.query.all()
        if not tasks:
            return {"error_message": "Task not Found"}, 404
        list_of_task = []
        for task in tasks:
            task_data = {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "purpose": task.purpose.value,
                "priority": task.priority.value,
                "due_date": task.due_date
            }
            list_of_task.append(task_data)

        return {
            "message": "Tasks List",
            "tasks": list_of_task
        }, 200
    if not user:
        return {"error_message": "User not Found"}, 404
    
    tasks = task_service.get_by_user_id(user_id)

    list_of_task = []
    for task in tasks:
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "purpose": task.purpose.value,
            "priority": task.priority.value,
            "due_date": task.due_date
        }
        list_of_task.append(task_data)

    return {
        "message": f"{user.name}'s Tasks List",
        "tasks": list_of_task
    }, 200

class EditTaskSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    purpose = fields.Enum(TaskPurpose, required=True)
    priority = fields.Enum(TaskPriority, required=True)
    due_date = fields.DateTime(format=DUE_DATE_FORMAT, required=True)

@task_blueprint.route('/edit/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    data = request.get_json()
    schema = EditTaskSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400
    
    task = task_service.get_by_id(task_id)

    if not task:
        return {"error_message": "Task not Found."}, 404
    
    if task.user_id != user.id:
        return {"error_message": "Unauthorized. You can only edit your own task."}, 403

    if len(data['description']) > 150:
        return {"error_message": "Description Can't be longer than 150 characters"}, 400

    result = task_service.edit(
        task_id=task_id,
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        purpose=data['purpose'],
        priority=data['priority'],
        due_date = data['due_date']
    )

    return result

class UpdateTaskStatusSchema(Schema):
    status = fields.Enum(TaskStatus, required=True)

@task_blueprint.route('/update/<int:task_id>', methods=['PATCH'])
def update_task_status(task_id):
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']
    user = user_service.get_by_id(user_id)

    data = request.get_json()
    schema = UpdateTaskStatusSchema()
    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400
    
    task = task_service.get_by_id(task_id)
    staff_or_admin = token_payload['role'] == 'STAFF' or token_payload['role'] == 'ADMIN'

    if staff_or_admin:
        task_service.update(task_id, user_id, status=data['status'])
        updated_task = task_service.get_by_id(task_id)  
        return {"message": f"Task Status Successfully Updated to {updated_task.status.value} by {user.role.value}"}, 200

    if not user:
        return {"error_message": "User not Found"}, 404


    if task.user_id != user_id:
        return {"error_message": "Unauthorized. You can only update your own tasks."}, 403

    task_service.update(task_id, user_id, status=data['status'])
    updated_task = task_service.get_by_id(task_id)
    return {
        "message": f"Task Status Successfully Updated to {updated_task.status.value}"
    }, 200

@task_blueprint.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    staff_or_admin = token_payload['role'] == 'STAFF' or token_payload['role'] == 'ADMIN'

    if staff_or_admin:
        task_service.delete(task_id, user_id)
        return {"message": f"Task successfully deleted by {user.role.value}"}, 200

    if not user:
        return {"error_message": "User not Found"}, 404

    task = task_service.get_by_id(task_id)

    if task.user_id != user.id:
        return {"error message": f"Task doesn't belong to {user.name}"}, 400
    
    task_service.delete(task_id, user_id)

    return {"message": f"Task successfully deleted by {user.name}"}, 200