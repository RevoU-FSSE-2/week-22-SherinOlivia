from core.user.models import UserDomain
from core.common.utils import ObjectMapperUtil
from core.user.ports import IUserAccessor
from infrastructure.db import db
from infrastructure.user.models import User
from typing import Optional

class UserAccessor(IUserAccessor):

    def create(self, username: str, email: str, hashed_password: str, name: str, city: str, about_me: str, role: str)  -> UserDomain:
        new_user = User(username=username, email=email, password=hashed_password, name=name, city=city, about_me=about_me, role=role)
        db.session.add(new_user)
        db.session.commit()

        return ObjectMapperUtil.map(new_user, UserDomain)
        
    def get_by_username(self, username: str)  -> Optional[UserDomain]:
        user = User.query.filter_by(username=username).first()
        return ObjectMapperUtil.map(user, UserDomain)
    
    def get_by_id(self, user_id: int)  -> Optional[UserDomain]:
        user = User.query.get(user_id)
        return ObjectMapperUtil.map(user, UserDomain)