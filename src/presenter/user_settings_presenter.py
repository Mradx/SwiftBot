from aiogram.types import InlineKeyboardMarkup

from src.config import PAGINATION_LIMIT
from src.handlers.keyboards import kb_language, kb_confirm_update_language
from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.repositories.translations_repository import TranslationsRepository
from src.repositories.user_settings_repository import UserSettingsRepository
from src.utils.translator import Translator


class UserSettingsPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User, translations_repo: TranslationsRepository,
                 user_settings_repo: UserSettingsRepository):
        super().__init__(translator, user)
        self.__translations_repo = translations_repo
        self.__user_settings_repo = user_settings_repo

    async def get_user_language(self):
        return self.__user_settings_repo.get_user_language()

    async def set_user_language(self, lang_name):
        if lang_name in self.__translations_repo.get_translation_names_all():
            await self.__user_settings_repo.save_user_language(lang_name)
            return self.translator("language_updated", lang_name=self.translator(lang_name))
        else:
            return self.translator("language_no_available", lang_name=self.translator(lang_name))

    async def get_languages_list_for_load(self, current_page: int = 1) -> [str, InlineKeyboardMarkup]:
        offset = (current_page - 1) * PAGINATION_LIMIT
        lang_names, total_pages = self.__translations_repo.get_translation_names(
            limit=PAGINATION_LIMIT,
            offset=offset
        )

        if not lang_names:
            return self.translator("languages_no_available"), None

        if current_page == 1:
            return (
                self.translator("choose_language"),
                kb_language(self.get_translator(), lang_names, total_pages)
            )
        else:
            return None, kb_language(self.get_translator(), lang_names, total_pages, current_page)

    async def confirm_update_language(self, lang_name: str) -> [str | InlineKeyboardMarkup]:
        lang_names = self.__translations_repo.get_translation_names_all()

        if lang_name not in lang_names:
            return self.translator("language_no_available", lang_name=lang_name), None

        return (self.translator("confirm_update_language", lang_name=self.translator(lang_name)),
                kb_confirm_update_language(self.get_translator(), lang_name))
