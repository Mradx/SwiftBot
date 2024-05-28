from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.handlers.keyboards import kb_cancel_and_delete_msg
from src.presenter.chat_editor_presenter import ChatEditorPresenter


async def update_chat_editor_last_response_command(message: types.Message, state: FSMContext,
                                                   chat_editor_presenter: ChatEditorPresenter):
    await message.delete()

    new_message = await message.answer(
        text=chat_editor_presenter.translator("enter_text_to_update_last_message"),
        reply_markup=kb_cancel_and_delete_msg(chat_editor_presenter.get_translator()))
    await state.update_data(chat_editor_presenter.create_user_data_entry(
        data_key=StateDataKey.UPDATE_LAST_RESPONSE,
        value=str(new_message.message_id)))
    await state.set_state(States.update_last_response)


def register_handlers(dp: Dispatcher):
    dp.message.register(update_chat_editor_last_response_command, Command(commands=["edit"]))
