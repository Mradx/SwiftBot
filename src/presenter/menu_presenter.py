import logging

from src.handlers.keyboards import kb_menu
from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.repositories.gemini_repository import GeminiRepository
from src.repositories.user_history_repository import UserHistoryRepository
from src.utils.translator import Translator


class MenuPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User, user_history_repo: UserHistoryRepository,
                 gemini_repo: GeminiRepository):
        super().__init__(translator, user)
        self.__user_history_repo = user_history_repo
        self.__gemini_repo = gemini_repo

    async def show_menu(self):
        chat_histories = self.__user_history_repo.get_histories()
        history, system_instruction = self.__user_history_repo.load_history()
        try:
            tokens = await self.__gemini_repo.count_tokens(history) if history else 0
        except Exception as e:
            logging.exception(str(e))
            tokens = 0

        info_text = self.translator("info_text",
                                    system_instruction=system_instruction or self._translator("not_set"),
                                    history_count=len(history),
                                    tokens=tokens,
                                    saved_histories_count=len(chat_histories))

        return info_text, kb_menu(self.get_translator(), current_page=1)
