from dataclasses import dataclass
from datetime import datetime

from core.task.constants import TaskPriority, TaskPurpose, TaskStatus

@dataclass
class TaskDomain:
    id: int
    user_id: int
    title: str
    description: str
    purpose: TaskPurpose
    priority: TaskPriority
    status: TaskStatus
    due_date: datetime