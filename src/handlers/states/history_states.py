from aiogram import types, Dispatcher, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound
from aiogram.fsm.context import FSMContext

from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.presenter.history_presenter import HistoryPresenter


async def done_save_history_state(message: types.Message, state: FSMContext,
                                  history_presenter: HistoryPresenter, bot: Bot):
    data = await state.get_data()
    message_id = data.get(history_presenter.get_user_data_key(
        data_key=StateDataKey.SAVE_HISTORY))

    history_name = message.text
    await message.delete()

    text = await history_presenter.save_history(history_name)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=text,
            reply_markup=None
        )
    except (TelegramBadRequest, TelegramNotFound):
        await message.answer(text, reply_markup=None)

    await state.clear()


async def confirm_delete_history_state(message: types.Message, state: FSMContext,
                                       history_presenter: HistoryPresenter, bot: Bot):
    data = await state.get_data()
    message_id = data.get(history_presenter.get_user_data_key(
        data_key=StateDataKey.DELETE_HISTORY))

    history_name = message.text
    await message.delete()

    text, reply_markup = await history_presenter.confirm_delete_history(history_name)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup
        )
    except (TelegramBadRequest, TelegramNotFound):
        await message.answer(text, reply_markup=reply_markup)

    await state.clear()


def register_handlers(dp: Dispatcher):
    handlers = [
        (done_save_history_state, States.save_history),
        (confirm_delete_history_state, States.delete_history)
    ]

    for state, filter_ in handlers:
        dp.message.register(state, filter_)
