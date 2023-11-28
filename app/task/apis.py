from flask import Blueprint, request
from core.task.constants import TaskPurpose, TaskPriority
from core.task.services import TaskService
from core.user.services import UserService
from infrastructure.task.constants import DUE_DATE_FORMAT
from app.auth.utils import decode_jwt
from app.di import injector
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

task_blueprint = Blueprint('task', __name__)
task_service = injector.get(TaskService)
user_service = injector.get(UserService)

class CreateTaskSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    purpose = fields.Enum(TaskPurpose, required=True)
    priority = fields.Enum(TaskPriority, required=True)
    due_date = fields.DateTime(format=DUE_DATE_FORMAT, required=True)

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

class UpdateTaskSchema(Schema):
    task_id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    purpose = fields.Enum(TaskPurpose, required=True)
    priority = fields.Enum(TaskPriority, required=True)
    due_date = fields.DateTime(format=DUE_DATE_FORMAT, required=True)

@task_blueprint.route('/update', methods=['PUT'])
def update_task():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    data = request.get_json()
    schema = UpdateTaskSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400
    
    task = task_service.get_by_id(data['task_id'])

    if task.user_id != user_id:
        return {"error_message": "Unauthorized. You can only update your own tasks."}, 403

    if len(data['description']) > 150:
        return {"error_message": "Description Can't be longer than 150 characters"}, 400

    result = task_service.update(
        task_id=data['task_id'],
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        purpose=data['purpose'],
        priority=data['priority'],
        due_date = data['due_date']
    )

    return result