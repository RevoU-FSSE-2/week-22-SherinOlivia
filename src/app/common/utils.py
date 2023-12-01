import json
from flask import request
from functools import wraps
import bleach

def sanitize_input(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()

        json_string = json.dumps(data)

        sanitized_json = bleach.clean(str(json_string))
        sanitized_data = json.loads(sanitized_json)

        request.sanitized_data = sanitized_data

        return func(*args, **kwargs)

    return wrapper

def sanitize_url_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_id = request.view_args.get('task_id')

        sanitized_task_id = bleach.clean(str(task_id))

        request.sanitized_task_id = sanitized_task_id

        return func(*args, **kwargs)

    return wrapper
