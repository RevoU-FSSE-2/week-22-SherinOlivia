from enum import Enum

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TaskPurpose(Enum):
    WORK = "WORK"
    STUDY = "STUDY"
    GENERAL = "GENERAL"