from aiogram import types, Dispatcher, F

from src.callback_data.pagination_callback_data import PaginationCallbackData
from src.handlers.keyboards import kb_menu
from src.presenter.menu_presenter import MenuPresenter


async def menu_page_callback(callback_query: types.CallbackQuery, callback_data: PaginationCallbackData,
                             menu_presenter: MenuPresenter):
    current_page = callback_data.page
    inline_message_id = callback_query.inline_message_id

    await callback_query.message.edit_reply_markup(
        reply_markup=kb_menu(menu_presenter.get_translator(), current_page),
        inline_message_id=inline_message_id
    )


async def menu_callback(callback_query: types.CallbackQuery, menu_presenter: MenuPresenter):
    text, reply_markup = await menu_presenter.show_menu()
    await callback_query.message.answer(text, reply_markup=reply_markup)


def register_handlers(dp: Dispatcher):
    handlers = [
        (menu_page_callback, PaginationCallbackData.filter(F.action == PaginationCallbackData.Action.MENU_PAGE)),
        (menu_callback, PaginationCallbackData.filter(F.action == PaginationCallbackData.Action.MENU))
    ]

    for callback, filter_ in handlers:
        dp.callback_query.register(callback, filter_)
