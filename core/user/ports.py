from abc import ABC, abstractmethod
from core.user.models import UserDomain
from typing import Optional

class IUserAccessor(ABC):

    @abstractmethod
    def create(self, username: str, hashed_password: str, email: str, name: str, city: str, about_me: str, role: str) -> UserDomain:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserDomain]:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserDomain]:
        raise NotImplementedError