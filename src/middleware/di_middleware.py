from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types, Bot

from src.config import DEFAULT_LANGUAGE
from src.dependency_injection.di_manager import DependencyManager
from src.dependency_injection.presenter_factory import PresenterFactory
from src.models.user import User
from src.presenter.lazy_presenter import LazyPresenter


class DIMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, di_manager: DependencyManager):
        self.bot = bot
        self.di_manager = di_manager

    async def __call__(
            self,
            handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: Dict[str, Any],
    ) -> Any:
        user = self.get_user_data(event)

        user_history_repo = self.di_manager.get_user_history_repository(user.id, user.name)
        user_queue_repo = self.di_manager.get_user_queue_repository(user.id)
        gemini_repo = self.di_manager.get_gemini_repository()
        user_settings_repo = self.di_manager.get_user_settings_repository(user.id)
        translations_repo = self.di_manager.get_translations_repository()

        translator = await self.di_manager.get_translator(user)

        factory = PresenterFactory(translator, user, translations_repo, user_history_repo, user_queue_repo,
                                   gemini_repo, user_settings_repo)

        data.update({
            'bot': self.bot,
            'user_settings_presenter': LazyPresenter(factory.create_user_settings_presenter),
            'history_presenter': LazyPresenter(factory.create_history_presenter),
            'instruction_presenter': LazyPresenter(factory.create_instruction_presenter),
            'menu_presenter': LazyPresenter(factory.create_menu_presenter),
            'chat_editor_presenter': LazyPresenter(factory.create_chat_editor_presenter),
            'chat_presenter': LazyPresenter(factory.create_chat_presenter),
            'start_presenter': LazyPresenter(factory.create_start_presenter)
        })

        return await handler(event, data)

    @staticmethod
    def get_user_data(event: types.Update) -> User:
        user_id = None
        user_name = ""
        user_language = DEFAULT_LANGUAGE

        if event.event_type in ('message', 'callback_query'):
            user = getattr(event, event.event_type).from_user
            user_id = user.id
            user_name = user.first_name
            user_language = user.language_code
            if user.last_name:
                user_name += f" {user.last_name}"

        return User(user_id, user_name, user_language)
