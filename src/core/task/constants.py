from enum import Enum

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TaskPurpose(Enum):
    WORK = "WORK"
    STUDY = "STUDY"
    GENERAL = "GENERAL"
    PERSONAL = "PERSONAL"

class TaskStatus(Enum):
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"