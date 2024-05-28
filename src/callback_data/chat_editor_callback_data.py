from enum import Enum, auto

from aiogram.filters.callback_data import CallbackData


class ChatEditorCallbackData(CallbackData, prefix="chat_editor"):
    class Action(str, Enum):
        UPDATE_LAST = auto()

        def __str__(self):
            return self.name.lower()

    action: Action
