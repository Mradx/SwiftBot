from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.repositories.user_history_repository import UserHistoryRepository
from src.utils.translator import Translator


class ChatEditorPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User, user_history_repo: UserHistoryRepository):
        super().__init__(translator, user)
        self.__user_history_repo = user_history_repo

    async def update_last_response(self, new_response):
        if not self.__user_history_repo.has_previous_model_response():
            return self.translator("no_previous_model_responses")

        self.__user_history_repo.update_last_response(new_response)
        return self.translator("last_response_updated", new_response=new_response)
