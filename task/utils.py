from enum import IntEnum


class TaskStatus(IntEnum):
    RUNNING = 0
    IS_SCHEDULED = 1
    FAILED = 2
    ABORTED = 3
    FINISHED = 4

    @classmethod
    def get_choices(cls):
        return [(key.value, key.name) for key in cls]
