from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from src.callback_data.history_callback_data import HistoryCallbackData
from src.callback_data.pagination_callback_data import PaginationCallbackData
from src.fsm.state_data_key import StateDataKey
from src.fsm.states import States
from src.handlers.keyboards import kb_cancel_and_delete_msg, kb_confirm_clear_history
from src.presenter.history_presenter import HistoryPresenter


async def save_history_callback(callback_query: types.CallbackQuery, state: FSMContext,
                                history_presenter: HistoryPresenter):
    new_message = await callback_query.message.answer(history_presenter.translator("enter_history_name_to_save"),
                                                      reply_markup=kb_cancel_and_delete_msg(history_presenter.get_translator()))
    await state.update_data(history_presenter.create_user_data_entry(
        data_key=StateDataKey.SAVE_HISTORY,
        value=str(new_message.message_id)))
    await state.set_state(States.save_history)


async def show_histories_for_load_callback(callback_query: types.CallbackQuery, history_presenter: HistoryPresenter):
    text, reply_markup = await history_presenter.get_history_list_for_load()
    await callback_query.message.answer(text, reply_markup=reply_markup)


async def show_histories_for_load_page_callback(callback_query: types.CallbackQuery,
                                                callback_data: PaginationCallbackData,
                                                history_presenter: HistoryPresenter):
    current_page = callback_data.page
    inline_message_id = callback_query.inline_message_id

    text, reply_markup = await history_presenter.get_history_list_for_load(current_page)
    await callback_query.message.edit_reply_markup(
        reply_markup=reply_markup,
        inline_message_id=inline_message_id
    )


async def confirm_load_history_callback(callback_query: types.CallbackQuery,
                                        callback_data: HistoryCallbackData,
                                        history_presenter: HistoryPresenter):
    history_name = callback_data.history_name

    text, reply_markup = await history_presenter.confirm_load_history(history_name)
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


async def done_load_history_callback(callback_query: types.CallbackQuery, callback_data: HistoryCallbackData,
                                     history_presenter: HistoryPresenter):
    history_name = callback_data.history_name

    text = await history_presenter.load_history(history_name)
    await callback_query.message.edit_text(text)


async def show_histories_for_delete_callback(callback_query: types.CallbackQuery, history_presenter: HistoryPresenter):
    text, reply_markup = await history_presenter.get_history_list_for_delete()
    await callback_query.message.answer(text, reply_markup=reply_markup)


async def show_histories_for_delete_page_callback(callback_query: types.CallbackQuery,
                                                  callback_data: PaginationCallbackData,
                                                  history_presenter: HistoryPresenter):
    current_page = callback_data.page
    inline_message_id = callback_query.inline_message_id

    text, reply_markup = await history_presenter.get_history_list_for_delete(current_page)
    await callback_query.message.edit_reply_markup(
        reply_markup=reply_markup,
        inline_message_id=inline_message_id
    )


async def confirm_delete_history_callback(callback_query: types.CallbackQuery,
                                          callback_data: HistoryCallbackData,
                                          history_presenter: HistoryPresenter):
    history_name = callback_data.history_name

    text, reply_markup = await history_presenter.confirm_delete_history(history_name)
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


async def done_delete_history_callback(callback_query: types.CallbackQuery, callback_data: HistoryCallbackData,
                                       history_presenter: HistoryPresenter):
    history_name = callback_data.history_name

    text = await history_presenter.delete_history(history_name)
    await callback_query.message.edit_text(text)


async def confirm_clear_history_callback(callback_query: types.CallbackQuery, history_presenter: HistoryPresenter):
    await callback_query.message.answer(history_presenter.translator("confirm_clear_history"),
                                        reply_markup=kb_confirm_clear_history(history_presenter.get_translator()))


async def done_clear_history_callback(callback_query: types.CallbackQuery, history_presenter: HistoryPresenter):
    text = await history_presenter.clear_history()
    await callback_query.message.edit_text(text, reply_markup=None)


def register_handlers(dp: Dispatcher):
    handlers = [
        (save_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.SAVE)),
        (show_histories_for_load_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.LOAD)),
        (show_histories_for_load_page_callback, PaginationCallbackData.filter(F.action == PaginationCallbackData.Action.HISTORY_LOAD)),
        (confirm_load_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.LOAD_CONFIRM)),
        (done_load_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.LOAD_DONE)),
        (show_histories_for_delete_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.DELETE)),
        (show_histories_for_delete_page_callback, PaginationCallbackData.filter(F.action == PaginationCallbackData.Action.HISTORY_DELETE)),
        (confirm_delete_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.DELETE_CONFIRM)),
        (done_delete_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.DELETE_DONE)),
        (confirm_clear_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.CLEAR_CONFIRM)),
        (done_clear_history_callback, HistoryCallbackData.filter(F.action == HistoryCallbackData.Action.CLEAR_DONE))
    ]

    for callback, filter_ in handlers:
        dp.callback_query.register(callback, filter_)
