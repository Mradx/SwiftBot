from src.models.user import User
from src.presenter.chat_editor_presenter import ChatEditorPresenter
from src.presenter.history_presenter import HistoryPresenter
from src.presenter.instruction_presenter import InstructionPresenter
from src.presenter.menu_presenter import MenuPresenter
from src.presenter.chat_presenter import ChatPresenter
from src.presenter.start_presenter import StartPresenter
from src.presenter.user_settings_presenter import UserSettingsPresenter
from src.utils.translator import Translator


class PresenterFactory:
    def __init__(self, translator: Translator, user: User, translations_repo, user_history_repo, user_queue_repo,
                 gemini_repo, user_settings_repo):
        self.translator = translator
        self.user = user
        self.translations_repo = translations_repo
        self.user_history_repo = user_history_repo
        self.user_queue_repo = user_queue_repo
        self.gemini_repo = gemini_repo
        self.user_settings_repo = user_settings_repo

    def create_user_settings_presenter(self):
        return UserSettingsPresenter(self.translator, self.user, self.translations_repo, self.user_settings_repo)

    def create_history_presenter(self):
        return HistoryPresenter(self.translator, self.user, self.user_history_repo, self.user_queue_repo)

    def create_instruction_presenter(self):
        return InstructionPresenter(self.translator, self.user, self.user_history_repo)

    def create_menu_presenter(self):
        return MenuPresenter(self.translator, self.user, self.user_history_repo, self.gemini_repo)

    def create_chat_editor_presenter(self):
        return ChatEditorPresenter(self.translator, self.user, self.user_history_repo)

    def create_chat_presenter(self):
        return ChatPresenter(self.translator, self.user, self.user_history_repo, self.user_queue_repo,
                             self.gemini_repo)

    def create_start_presenter(self):
        return StartPresenter(self.translator, self.user)
