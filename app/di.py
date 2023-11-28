from injector import Injector
from infrastructure.user.modules import UserModule
from infrastructure.auth.modules import HashingModule
from infrastructure.task.modules import TaskModule

injector = Injector([
    UserModule,
    HashingModule,
    TaskModule
])