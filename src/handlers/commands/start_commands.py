import asyncio
import os

from aiogram import Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

from src.config import IMAGES_PATH, GITHUB_REPO_URL
from src.handlers.keyboards import kb_show_menu
from src.presenter.start_presenter import StartPresenter

IMAGE_START_PATH = 'start.jpg'


async def start_handler(message: types.Message, start_presenter: StartPresenter) -> None:
    await message.answer_photo(photo=FSInputFile(os.path.join(IMAGES_PATH, IMAGE_START_PATH)),
                               caption=start_presenter.translator("start_message", github_repo_url=GITHUB_REPO_URL),
                               reply_markup=kb_show_menu(start_presenter.get_translator()))
    await asyncio.sleep(2)
    await message.answer(start_presenter.translator("begin_chat"))


def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, CommandStart())
