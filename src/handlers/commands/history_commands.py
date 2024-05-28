from aiogram import Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.handlers.keyboards import kb_cancel_and_delete_msg
from src.presenter.history_presenter import HistoryPresenter


async def save_command(message: types.Message, command: CommandObject, state: FSMContext,
                       history_presenter: HistoryPresenter):
    history_name = command.args
    await message.delete()

    if not history_name:
        new_message = await message.answer(history_presenter.translator("enter_history_name_to_save"),
                                           reply_markup=kb_cancel_and_delete_msg(history_presenter.get_translator()))
        await state.update_data(history_presenter.create_user_data_entry(
            data_key=StateDataKey.SAVE_HISTORY,
            value=str(new_message.message_id)))
        await state.set_state(States.save_history)
        return

    text = await history_presenter.save_history(history_name)
    await message.answer(text)


async def delete_command(message: types.Message, command: CommandObject, history_presenter: HistoryPresenter):
    history_name = command.args
    await message.delete()

    if not history_name:
        text, reply_markup = await history_presenter.get_history_list_for_delete()
        await message.answer(text, reply_markup=reply_markup)
        return

    text, reply_markup = await history_presenter.confirm_delete_history(history_name)
    await message.answer(text, reply_markup=reply_markup)


async def load_command(message: types.Message, command: CommandObject, history_presenter: HistoryPresenter):
    history_name = command.args
    await message.delete()

    if not history_name:
        text, reply_markup = await history_presenter.get_history_list_for_load()
        await message.answer(text, reply_markup=reply_markup)
        return

    text = await history_presenter.load_history(history_name)
    await message.answer(text)


async def clear_command(message: types.Message, history_presenter: HistoryPresenter):
    await message.delete()

    text = await history_presenter.clear_history()
    await message.answer(text)


def register_handlers(dp: Dispatcher):
    handlers = [
        (save_command, Command(commands=["save"])),
        (delete_command, Command(commands=["delete"])),
        (load_command, Command(commands=["load"])),
        (clear_command, Command(commands=["clear"]))
    ]

    for command, filter_ in handlers:
        dp.message.register(command, filter_)
