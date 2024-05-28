from enum import Enum, auto

from aiogram.filters.callback_data import CallbackData


class CancelCallbackData(CallbackData, prefix="cancel"):
    class Action(str, Enum):
        DEL_MSG = auto()
        DEL_MSG_CLEAR_STATE = auto()

        def __str__(self):
            return self.name.lower()

    action: Action
