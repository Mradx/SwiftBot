from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.utils.translator import Translator


class StartPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User):
        super().__init__(translator, user)
        self.__translator = translator
