from aiogram import Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from src.presenter.user_settings_presenter import UserSettingsPresenter


async def update_language(message: types.Message, command: CommandObject,
                          user_settings_presenter: UserSettingsPresenter):
    language = command.args
    await message.delete()

    if not language:
        text, reply_markup = await user_settings_presenter.get_languages_list_for_load()
        await message.answer(text, reply_markup=reply_markup)
        return

    text = await user_settings_presenter.set_user_language(language)
    await message.answer(text)


def register_handlers(dp: Dispatcher):
    dp.message.register(update_language, Command(commands=["language", "lang"]))
