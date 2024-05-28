from aiogram import Dispatcher, types
from aiogram.filters import Command

from src.presenter.menu_presenter import MenuPresenter


async def menu_command(message: types.Message, menu_presenter: MenuPresenter):
    await message.delete()

    text, reply_markup = await menu_presenter.show_menu()
    await message.answer(text, reply_markup=reply_markup)


def register_handlers(dp: Dispatcher):
    dp.message.register(menu_command, Command(commands=["menu"]))
