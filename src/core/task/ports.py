from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from core.task.models import TaskDomain

class ITaskAccessor(ABC):

    @abstractmethod
    def create(self, user_id: int, title: str, description: str, purpose: str, priority: str, status: str, due_date: datetime) -> TaskDomain:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[TaskDomain]:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskDomain]:
        raise NotImplementedError
    
    @abstractmethod
    def edit(self, task_id: int, user_id: int, title: str, description: str, purpose: str, priority: str, due_date: datetime) -> Optional[TaskDomain]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, task_id: int, user_id: int, status: str) -> Optional[TaskDomain]:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, task_id: int, user_id: int) -> Optional[TaskDomain]:
        raise NotImplementedError
