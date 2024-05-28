from aiogram.types import InlineKeyboardMarkup

from src.config import PAGINATION_LIMIT
from src.handlers.keyboards import (kb_confirm_delete_history, kb_confirm_load_history, kb_history_for_load,
                                    kb_history_for_delete)
from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.repositories.user_history_repository import UserHistoryRepository
from src.repositories.user_queue_repository import UserQueueRepository
from src.utils.translator import Translator


class HistoryPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User, user_history_repo: UserHistoryRepository,
                 user_queue_repo: UserQueueRepository):
        super().__init__(translator, user)
        self.__user_history_repo = user_history_repo
        self.__user_queue_repo = user_queue_repo

    async def save_history(self, history_name: str) -> str:
        if len(history_name) > 20:
            return self.translator("history_name_too_long", length=len(history_name))

        history_count = len(self.__user_history_repo.get_history_names_all())
        if history_count >= 20:
            return self.translator("history_limit_reached")

        self.__user_history_repo.save_history(history_name=history_name)
        return self.translator("history_saved", history_name=history_name)

    async def confirm_delete_history(self, history_name: str) -> [str | InlineKeyboardMarkup]:
        history_names = self.__user_history_repo.get_history_names_all()
        if history_name not in history_names:
            return self.translator("history_not_found", history_name=history_name), None

        return (self.translator("confirm_delete_history", history_name=history_name),
                kb_confirm_delete_history(self.get_translator(), history_name))

    async def delete_history(self, history_name: str) -> [str | InlineKeyboardMarkup]:
        self.__user_history_repo.delete_history(history_name)
        return self.translator("history_deleted", history_name=history_name)

    async def confirm_load_history(self, history_name: str) -> [str | InlineKeyboardMarkup]:
        history_names = self.__user_history_repo.get_history_names_all()
        if history_name not in history_names:
            return self.translator("history_not_found", history_name=history_name), None

        return (self.translator("confirm_load_history", history_name=history_name),
                kb_confirm_load_history(self.get_translator(), history_name))

    async def load_history(self, history_name: str) -> str:
        chat_histories = self.__user_history_repo.get_histories()

        if history_name not in chat_histories:
            return self.translator("history_not_found", history_name=history_name)

        self.__user_history_repo.load_history(history_name)
        return self.translator("history_loaded", history_name=history_name)

    async def get_history_list_for_load(self, current_page: int = 1) -> [str, InlineKeyboardMarkup]:
        offset = (current_page - 1) * PAGINATION_LIMIT
        history_names, total_pages = self.__user_history_repo.get_history_names(
            limit=PAGINATION_LIMIT,
            offset=offset
        )

        if not history_names:
            return self.translator("no_saved_histories"), None

        if current_page == 1:
            return (
                self.translator("choose_history_to_load"),
                kb_history_for_load(self.get_translator(), history_names, total_pages)
            )
        else:
            return None, kb_history_for_load(self.get_translator(), history_names, total_pages, current_page)

    async def get_history_list_for_delete(self, current_page: int = 1) -> [str, InlineKeyboardMarkup]:
        offset = (current_page - 1) * PAGINATION_LIMIT
        history_names, total_pages = self.__user_history_repo.get_history_names(
            limit=PAGINATION_LIMIT,
            offset=offset
        )

        if not history_names:
            return self.translator("no_saved_histories"), None

        if current_page == 1:
            return (self.translator("choose_history_to_delete"),
                    kb_history_for_delete(self.get_translator(), history_names, total_pages))
        else:
            return None, kb_history_for_delete(self.get_translator(), history_names, total_pages, current_page)

    async def clear_history(self) -> str:
        self.__user_queue_repo.clear_queue()
        self.__user_queue_repo.set_processing_task(None)

        self.__user_history_repo.clear_history()
        return self.translator("history_and_instructions_cleared")
