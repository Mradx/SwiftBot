from aiogram import types, F, Dispatcher
from aiogram.fsm.context import FSMContext

from src.callback_data.cancel_callback_data import CancelCallbackData


async def del_msg_callback(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


async def del_msg_clear_state_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.clear()


def register_handlers(dp: Dispatcher):
    handlers = [
        (del_msg_callback, CancelCallbackData.filter(F.action == CancelCallbackData.Action.DEL_MSG)),
        (del_msg_clear_state_callback, CancelCallbackData.filter(F.action == CancelCallbackData.Action.DEL_MSG_CLEAR_STATE))
    ]

    for callback, filter_ in handlers:
        dp.callback_query.register(callback, filter_)
