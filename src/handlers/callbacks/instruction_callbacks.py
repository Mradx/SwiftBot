from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from src.callback_data.instruction_callback_data import InstructionCallbackData
from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.handlers.keyboards import kb_cancel_and_delete_msg
from src.presenter.instruction_presenter import InstructionPresenter


async def update_instruction_callback(callback_query: types.CallbackQuery, state: FSMContext,
                                      instruction_presenter: InstructionPresenter):
    new_message = await callback_query.message.answer(
        text=instruction_presenter.translator("enter_new_instruction"),
        reply_markup=kb_cancel_and_delete_msg(instruction_presenter.get_translator()))
    await state.update_data(instruction_presenter.create_user_data_entry(
        data_key=StateDataKey.UPDATE_INSTRUCTION,
        value=str(new_message.message_id)))
    await state.set_state(States.update_instruction)


def register_handlers(dp: Dispatcher):
    dp.callback_query.register(update_instruction_callback, InstructionCallbackData.filter(F.action == InstructionCallbackData.Action.UPDATE))
