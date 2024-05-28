from aiogram import Dispatcher, types, Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNotFound
from aiogram.fsm.context import FSMContext

from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.presenter.chat_editor_presenter import ChatEditorPresenter


async def done_chat_editor_last_response_state(message: types.Message, state: FSMContext,
                                               chat_editor_presenter: ChatEditorPresenter, bot: Bot):
    data = await state.get_data()
    message_id = data.get(chat_editor_presenter.get_user_data_key(
        data_key=StateDataKey.UPDATE_LAST_RESPONSE))

    new_response = message.text
    await message.delete()

    text = await chat_editor_presenter.update_last_response(new_response)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=text,
            reply_markup=None
        )
    except (TelegramBadRequest, TelegramNotFound):
        await message.answer(text)

    await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(done_chat_editor_last_response_state, States.update_last_response)
