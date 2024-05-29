from bs4 import BeautifulSoup
from aiogram.types import ContentType
from google.api_core.exceptions import ResourceExhausted

from src.models.user import User
from src.presenter.base_presenter import BasePresenter
from src.repositories.gemini_repository import GeminiRepository
from src.repositories.user_history_repository import UserHistoryRepository
from src.repositories.user_queue_repository import UserQueueRepository
from src.utils.md_parser import format_text
from src.utils.file_parser import process_file
from src.utils.translator import Translator

content_type_handlers = {
    ContentType.PHOTO: lambda m: m.photo[-1],
    ContentType.AUDIO: lambda m: m.audio,
    ContentType.VOICE: lambda m: m.voice,
    ContentType.DOCUMENT: lambda m: m.document,
    ContentType.STICKER: lambda m: m.sticker.thumbnail
}


class ChatPresenter(BasePresenter):
    def __init__(self, translator: Translator, user: User, user_history_repo: UserHistoryRepository,
                 user_queue_repo: UserQueueRepository, gemini_repo: GeminiRepository):
        super().__init__(translator, user)
        self.__user_history_repo = user_history_repo
        self.__user_queue_repo = user_queue_repo
        self.__gemini_repo = gemini_repo

    @staticmethod
    async def get_media_input(translator, bot, message, get_file_id_func):
        file_size = get_file_id_func(message).file_size
        if file_size > 20 * 1024 * 1024:
            raise ValueError(translator("file_size_exceeded"))
        file_id = get_file_id_func(message).file_id
        try:
            user_input = await process_file(translator, bot, file_id)
        except ValueError as e:
            raise ValueError(str(e))

        return user_input

    @staticmethod
    def extract_forward_sender_name(message):
        try:
            user = message.forward_from
            user_name = user.first_name
            if user.last_name:
                user_name += f" {user.last_name}"
        except:
            user_name = None

        return user_name

    async def parse_message_content(self, bot, message, is_reply_or_forwarded=False):
        reply_text = ""

        if is_reply_or_forwarded:
            user_name = self.extract_forward_sender_name(message)

            if user_name:
                reply_text = self.translator("forwarded_message_from", user_name=user_name)
            else:
                reply_text = self.translator("forwarded_message")

        if message.content_type in content_type_handlers:
            try:
                forward_input = await self.get_media_input(self.translator, bot, message,
                                                           content_type_handlers[message.content_type])
            except ValueError as e:
                raise ValueError(str(e))

            if message.caption:
                forward_input = [reply_text + message.caption, forward_input] if is_reply_or_forwarded \
                    else [message.caption, forward_input]
            else:
                forward_input = [reply_text, forward_input] if is_reply_or_forwarded \
                    else [forward_input]

        else:
            forward_input = [reply_text + message.text] if is_reply_or_forwarded \
                else [message.text]

        return forward_input

    async def prepare_gemini_input(self, message, bot):
        try:
            user_input = None
            forward_input = None
            gemini_inputs: list = []

            try:
                if message.reply_to_message:
                    forward_input = await self.parse_message_content(bot, message.reply_to_message, True)
                elif message.forward_origin:
                    forward_input = await self.parse_message_content(bot, message, True)
            except ValueError as e:
                raise ValueError(str(e))

            try:
                if not message.forward_origin:
                    user_input = await self.parse_message_content(bot, message)
            except ValueError as e:
                raise ValueError(str(e))

            if user_input:
                gemini_inputs.append(user_input)

            if forward_input:
                gemini_inputs.append(forward_input)

            if len(gemini_inputs) == 0:
                raise ValueError(self.translator("no_response"))

            return gemini_inputs

        except ValueError as e:
            raise ValueError(str(e))

        except (ResourceExhausted, Exception) as e:
            raise ValueError(str(e))

    async def generate_gemini_response(self, gemini_inputs: list) -> str:
        history, system_instruction = self.__user_history_repo.load_history()
        response = await self.__gemini_repo.generate_content(
            history, system_instruction, gemini_inputs,
            self.get_user_language())

        if not response.candidates:
            raise ValueError(self.translator("no_response"))

        for user_input in gemini_inputs:
            self.__user_history_repo.add_message("user", user_input)
        self.__user_history_repo.add_message("model", response.text)

        response = format_text(response.text)
        BeautifulSoup(response, "html.parser")

        return response

    async def get_inputs_to_process(self):
        user_queue = self.get_user_queue()
        inputs_to_process = []
        for task, _ in user_queue.get_queue():
            input_data = await task
            inputs_to_process.extend(input_data)
        return inputs_to_process

    def get_user_queue(self):
        return self.__user_queue_repo

    def get_processing_task(self):
        return self.__user_queue_repo.get_processing_task()

    def set_processing_task(self, task):
        self.__user_queue_repo.set_processing_task(task)

    def get_error_message_id(self):
        return self.__user_queue_repo.get_error_message_id()

    def set_error_message_id(self, error_message_id):
        self.__user_queue_repo.set_error_message_id(error_message_id)

    def cancel_processing_task(self):
        self.__user_queue_repo.cancel_processing_task()

    def add_task(self, task):
        self.__user_queue_repo.add_task(task)

    def clear_user_queue(self):
        self.__user_queue_repo.clear_queue()

    def reset_queue_and_task(self):
        self.__user_queue_repo.clear_queue()
        self.__user_queue_repo.cancel_processing_task()
