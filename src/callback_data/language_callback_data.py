from enum import Enum, auto

from aiogram.filters.callback_data import CallbackData


class LanguageCallbackData(CallbackData, prefix="language"):
    class Action(str, Enum):
        UPDATE = auto()
        UPDATE_CONFIRM = auto()
        UPDATE_DONE = auto()

        def __str__(self):
            return self.name.lower()

    action: Action
    lang_name: str | None
