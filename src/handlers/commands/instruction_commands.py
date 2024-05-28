from aiogram import Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.handlers.keyboards import kb_cancel_and_delete_msg
from src.presenter.instruction_presenter import InstructionPresenter


async def update_instruction_command(message: types.Message, command: CommandObject, state: FSMContext,
                                     instruction_presenter: InstructionPresenter):
    new_instruction = command.args
    await message.delete()

    if not new_instruction:
        new_message = await message.answer(
            text=instruction_presenter.translator("enter_new_instruction"),
            reply_markup=kb_cancel_and_delete_msg(instruction_presenter.get_translator()))
        await state.update_data(instruction_presenter.create_user_data_entry(
            data_key=StateDataKey.UPDATE_INSTRUCTION,
            value=str(new_message.message_id)))
        await state.set_state(States.update_instruction)
        return

    text = await instruction_presenter.update_instruction(new_instruction)
    await message.answer(text)


async def delete_instruction_command(message: types.Message, instruction_presenter: InstructionPresenter):
    await message.delete()

    text = await instruction_presenter.delete_instruction()
    await message.answer(text)


def register_handlers(dp: Dispatcher):
    handlers = [
        (update_instruction_command, Command(commands=["setinst"])),
        (delete_instruction_command, Command(commands=["delinst"]))
    ]

    for command, filter_ in handlers:
        dp.message.register(command, filter_)
