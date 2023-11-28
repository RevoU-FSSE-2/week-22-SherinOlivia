from dataclasses import dataclass
from datetime import datetime

from core.task.constants import TaskPriority, TaskPurpose

@dataclass
class TaskDomain:
    id: int
    user_id: int
    title: str
    purpose: TaskPurpose
    description: str
    due_date: datetime
    priority: TaskPriority
    is_deleted: bool