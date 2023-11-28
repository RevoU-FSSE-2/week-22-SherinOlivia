from dataclasses import dataclass
from core.user.constants import UserRole

@dataclass
class UserDomain:
    id: int
    username: str
    email: str
    password: str
    name: str
    city: str
    about_me: str
    role: UserRole

