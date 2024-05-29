from src.models.user import User
from src.utils.translator import Translator


class BasePresenter:
    def __init__(self, translator: Translator, user: User):
        self._translator = translator
        self.__user_id = user.id
        self.__user_name = user.name
        self.__user_language = user.language

    def get_user_id(self):
        return self.__user_id

    def get_user_name(self):
        return self.__user_name

    def get_user_language(self):
        return self.__user_language

    def get_user_data_key(self, data_key: str) -> str:
        user_id = self.get_user_id()
        return f"{user_id}_{data_key}"

    def create_user_data_entry(self, data_key: str, value: str) -> dict[str, str]:
        key = self.get_user_data_key(data_key)
        return {key: value}

    def get_translator(self) -> Translator:
        return self._translator

    def translator(self, key, **kwargs):
        return self._translator(key, **kwargs)
