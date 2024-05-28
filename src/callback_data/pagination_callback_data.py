from enum import Enum, auto

from aiogram.filters.callback_data import CallbackData


class PaginationCallbackData(CallbackData, prefix="pagination"):
    class Action(str, Enum):
        MENU = auto()
        MENU_PAGE = auto()
        HISTORY_LOAD = auto()
        HISTORY_DELETE = auto()
        LANGUAGES = auto()

        def __str__(self):
            return self.name.lower()

    action: Action
    page: int
