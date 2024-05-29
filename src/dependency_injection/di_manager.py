from src.database.database_manager import DatabaseManager
from src.models.queue.user_queue_manager import UserQueueManager
from src.models.user import User
from src.repositories.gemini_repository import GeminiRepository
from src.repositories.translations_repository import TranslationsRepository
from src.repositories.user_history_repository import UserHistoryRepository
from src.repositories.user_settings_repository import UserSettingsRepository
from src.utils.translator import Translator


class DependencyManager:
    def __init__(self):
        self.user_settings_repositories = {}
        self.user_histories_repositories = {}
        self.user_queue_manager = UserQueueManager()
        self.gemini_repository = GeminiRepository()
        self.translations_repository = TranslationsRepository()
        self.database_manager = None

    def initialize_database(self):
        self.database_manager = DatabaseManager()
        self.database_manager.initialize()

    async def get_translator(self, user: User) -> Translator:
        user_settings_repo = self.get_user_settings_repository(user.id)
        user_custom_language = await user_settings_repo.get_user_language()
        user_language = user_custom_language if user_custom_language else user.language
        return Translator(user_language)

    def get_user_settings_repository(self, user_id):
        if user_id not in self.user_settings_repositories:
            self.user_settings_repositories[user_id] = UserSettingsRepository(user_id)
        return self.user_settings_repositories[user_id]

    def get_user_history_repository(self, user_id, user_name=None):
        if user_id not in self.user_histories_repositories:
            self.user_histories_repositories[user_id] = UserHistoryRepository(user_id, user_name)
        return self.user_histories_repositories[user_id]

    def get_user_queue_repository(self, user_id):
        return self.user_queue_manager.get_user_queue_repository(user_id)

    def get_gemini_repository(self):
        return self.gemini_repository

    def get_translations_repository(self):
        return self.translations_repository
