from enum import Enum, auto

from aiogram.filters.callback_data import CallbackData


class HistoryCallbackData(CallbackData, prefix="history"):
    class Action(str, Enum):
        SAVE = auto()
        LOAD = auto()
        LOAD_CONFIRM = auto()
        LOAD_DONE = auto()
        DELETE = auto()
        DELETE_CONFIRM = auto()
        DELETE_DONE = auto()
        CLEAR_CONFIRM = auto()
        CLEAR_DONE = auto()

        def __str__(self):
            return self.name.lower()

    action: Action
    history_name: str | None
