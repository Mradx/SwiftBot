from enum import Enum, auto

from aiogram.filters.callback_data import CallbackData


class InstructionCallbackData(CallbackData, prefix="instruction"):
    class Action(str, Enum):
        UPDATE = auto()

        def __str__(self):
            return self.name.lower()

    action: Action
