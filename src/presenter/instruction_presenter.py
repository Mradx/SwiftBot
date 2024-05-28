from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.repositories.user_history_repository import UserHistoryRepository
from src.utils.translator import Translator


class InstructionPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User, user_history_repo: UserHistoryRepository):
        super().__init__(translator, user)
        self.__translator = translator
        self.__user_history_repo = user_history_repo

    async def update_instruction(self, new_instruction):
        self.__user_history_repo.set_system_instruction(new_instruction)
        return self.translator("instruction_set", new_instruction=new_instruction)

    async def delete_instruction(self):
        self.__user_history_repo.set_system_instruction(None)
        return self.translator("instruction_cleared")
