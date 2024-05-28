from aiogram import types, Bot, Dispatcher
from aiogram.exceptions import TelegramNotFound, TelegramBadRequest
from aiogram.fsm.context import FSMContext

from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.presenter.instruction_presenter import InstructionPresenter


async def done_instruction_state(message: types.Message, state: FSMContext,
                                 instruction_presenter: InstructionPresenter, bot: Bot):
    data = await state.get_data()
    message_id = data.get(instruction_presenter.get_user_data_key(
        data_key=StateDataKey.UPDATE_INSTRUCTION))

    new_instruction = message.text
    await message.delete()

    text = await instruction_presenter.update_instruction(new_instruction)
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
    dp.message.register(done_instruction_state, States.update_instruction)
