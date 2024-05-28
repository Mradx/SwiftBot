from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from src.callback_data.chat_editor_callback_data import ChatEditorCallbackData
from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.handlers.keyboards import kb_cancel_and_delete_msg
from src.presenter.chat_editor_presenter import ChatEditorPresenter


async def update_chat_editor_last_response_callback(callback_query: types.CallbackQuery, state: FSMContext,
                                                    chat_editor_presenter: ChatEditorPresenter):
    new_message = await callback_query.message.answer(
        text=chat_editor_presenter.translator("enter_text_to_update_last_message"),
        reply_markup=kb_cancel_and_delete_msg(chat_editor_presenter.get_translator()))
    await state.update_data(chat_editor_presenter.create_user_data_entry(
        data_key=StateDataKey.UPDATE_LAST_RESPONSE,
        value=str(new_message.message_id)))
    await state.set_state(States.update_last_response)


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(update_chat_editor_last_response_callback,
                               ChatEditorCallbackData.filter(F.action == ChatEditorCallbackData.Action.UPDATE_LAST))
