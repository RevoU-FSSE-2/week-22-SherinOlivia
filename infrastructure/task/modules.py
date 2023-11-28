from injector import Module, singleton, Binder
from core.task.ports import ITaskAccessor
from infrastructure.task.adapters import TaskAccessor

class TaskModule(Module):

    def configure(self, binder: Binder) -> None:
        binder.bind(ITaskAccessor, to=TaskAccessor, scope=singleton)