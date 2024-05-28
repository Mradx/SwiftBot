import asyncio
import logging
import time

from aiogram import Dispatcher, types, Bot, F
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound
from aiogram.types import ContentType
from aiogram.utils.chat_action import ChatActionSender
from google.api_core.exceptions import ResourceExhausted

from src.config import RESPONSE_DELAY
from src.presenter.chat_presenter import ChatPresenter


class ChatHandler:
    def __init__(self, bot: Bot, chat_presenter: ChatPresenter):
        self.__bot = bot
        self.__chat_presenter = chat_presenter

    async def handle_gemini_request(self, message: types.Message) -> None:
        if self.__chat_presenter.get_processing_task():
            error_message_id = self.__chat_presenter.get_error_message_id()

            if error_message_id:
                await self.__bot.delete_message(chat_id=message.chat.id, message_id=error_message_id)
                self.__chat_presenter.set_error_message_id(None)

            self.__chat_presenter.cancel_processing_task()

        process_task = asyncio.create_task(self.__chat_presenter.prepare_gemini_input(message, self.__bot))
        self.__chat_presenter.add_task((process_task, time.time()))

        processing_task = asyncio.create_task(
            self.process_queue_after_delay(message, RESPONSE_DELAY, 0))

        self.__chat_presenter.set_processing_task(processing_task)

    async def process_queue_after_delay(self, message, delay, retry_count=0):
        try:
            error_message_id = self.__chat_presenter.get_error_message_id()

            if error_message_id:
                text = self.__chat_presenter.translator("retrying_please_wait")
                await self.send_or_update_message(message, text, error_message_id)

            if delay > 0:
                await asyncio.sleep(delay)

            inputs_to_process = await self.__chat_presenter.get_inputs_to_process()
            if inputs_to_process:
                async with ChatActionSender.typing(bot=self.__bot, chat_id=message.chat.id):
                    text = await self.__chat_presenter.generate_gemini_response(inputs_to_process)
                    try:
                        await message.answer(text)
                    except TelegramBadRequest:
                        await message.answer(text, parse_mode=None)

                self.__chat_presenter.reset_queue_and_task()

                if error_message_id:
                    await self.__bot.delete_message(chat_id=message.chat.id, message_id=error_message_id)
                    self.__chat_presenter.set_error_message_id(None)

        except ValueError as e:
            logging.error(f"Error: {str(e)}")

            self.__chat_presenter.reset_queue_and_task()

            await self.__bot.send_message(
                message.from_user.id,
                self.__chat_presenter.translator("error_occurred", error=str(e)),
                reply_to_message_id=message.message_id
            )

        except (ResourceExhausted, Exception) as e:
            logging.error(f"Error: {str(e)}")
            await self.retry_on_error(e, message, retry_count)

    async def retry_on_error(self, e, message, retry_count):
        error_message_id = self.__chat_presenter.get_error_message_id()
        retry_count += 1

        if retry_count > 5:
            self.__chat_presenter.reset_queue_and_task()

            text = self.__chat_presenter.translator("request_failed_try_later")
            await self.send_or_update_message(message, text, error_message_id)

            self.__chat_presenter.set_error_message_id(None)
            return

        delay = 2 ** retry_count
        if isinstance(e, ResourceExhausted):
            text = self.__chat_presenter.translator("api_quota_exceeded", delay=delay)
        else:
            text = self.__chat_presenter.translator("retrying_in_seconds", delay=delay)
        self.__chat_presenter.set_error_message_id(
            await self.send_or_update_message(message, text, error_message_id))

        await asyncio.sleep(delay)
        await self.process_queue_after_delay(message, 0, retry_count)

    async def send_or_update_message(self, message, text, message_id=None) -> int | None:
        try:
            if message_id is None:
                new_message = await self.__bot.send_message(
                    message.from_user.id, text, reply_to_message_id=message.message_id
                )
                return new_message.message_id
            else:
                await self.__bot.edit_message_text(
                    chat_id=message.chat.id, message_id=message_id, text=text
                )
                return message_id
        except (TelegramBadRequest, TelegramNotFound) as e:
            logging.error(f"Error: {str(e)}")
            new_message = await self.__bot.send_message(
                message.from_user.id, text, reply_to_message_id=message.message_id
            )
            return new_message.message_id


async def on_startup(message: types.Message, chat_presenter: ChatPresenter, bot: Bot):
    handler = ChatHandler(bot, chat_presenter)
    await handler.handle_gemini_request(message)


def register_handlers(dp: Dispatcher):
    dp.message.register(
        on_startup,
        F.content_type.in_({
            ContentType.TEXT,
            ContentType.PHOTO,
            ContentType.STICKER,
            ContentType.AUDIO,
            ContentType.VOICE,
            ContentType.DOCUMENT
        })
    )
