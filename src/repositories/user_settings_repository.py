from src.database.entities.user_settings import UserSettings


class UserSettingsRepository:
    def __init__(self, user_id: int):
        self.__user_id = user_id

    async def get_user_language(self):
        user_settings = UserSettings.objects(user_id=self.__user_id).first()
        return user_settings.language_code if user_settings else None

    async def save_user_language(self, language_code: str):
        user_settings = UserSettings.objects(user_id=self.__user_id).first()
        if not user_settings:
            user_settings = UserSettings(user_id=self.__user_id, language_code=language_code)
        else:
            user_settings.language_code = language_code
        user_settings.save()
