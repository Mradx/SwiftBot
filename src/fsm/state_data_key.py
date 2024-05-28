from enum import Enum, auto


class StateDataKey(str, Enum):
    SAVE_HISTORY = auto()
    DELETE_HISTORY = auto()
    UPDATE_INSTRUCTION = auto()
    UPDATE_LAST_RESPONSE = auto()
    UPDATE_LANGUAGE = auto()

    def __str__(self):
        return self.name.lower()
