import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import BOT_TOKEN, USE_PROXY, PROXY
from src.dependency_injection.di_manager import DependencyManager
from src.handlers import chat
from src.handlers.callbacks import (
    chat_editor_callbacks,
    history_callbacks,
    instruction_callbacks,
    menu_callbacks,
    common_callbacks,
    settings_callbacks,
)
from src.handlers.commands import (
    chat_editor_commands,
    instruction_commands,
    history_commands,
    menu_commands,
    start_commands,
    settings_commands,
)
from src.handlers.states import (
    history_states,
    instruction_states,
    chat_editor_states,
)
from src.middleware.chat_type_middleware import ChatTypeMiddleware
from src.middleware.di_middleware import DIMiddleware


def configure_proxy():
    if USE_PROXY and PROXY:
        os.environ['http_proxy'] = PROXY
        os.environ['https_proxy'] = PROXY


def register_handlers(dp: Dispatcher) -> None:
    commands = [
        start_commands, settings_commands, history_commands,
        instruction_commands, menu_commands, chat_editor_commands
    ]

    callbacks = [
        settings_callbacks, history_callbacks, instruction_callbacks,
        menu_callbacks, chat_editor_callbacks, common_callbacks
    ]

    states = [
        history_states, instruction_states, chat_editor_states
    ]

    others = [chat]

    for module in commands + callbacks + states + others:
        module.register_handlers(dp)


def register_middlewares(dp: Dispatcher, bot: Bot, di_manager: DependencyManager):
    dp.update.middleware(ChatTypeMiddleware())
    dp.update.middleware(DIMiddleware(bot, di_manager))


async def main():
    configure_proxy()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    di_manager = DependencyManager()
    di_manager.initialize_database()

    register_middlewares(dp, bot, di_manager)
    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
