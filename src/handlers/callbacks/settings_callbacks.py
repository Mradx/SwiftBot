from aiogram import types, Dispatcher, F

from src.callback_data.language_callback_data import LanguageCallbackData
from src.callback_data.pagination_callback_data import PaginationCallbackData
from src.presenter.user_settings_presenter import UserSettingsPresenter


async def show_languages_callback(callback_query: types.CallbackQuery, user_settings_presenter: UserSettingsPresenter):
    text, reply_markup = await user_settings_presenter.get_languages_list_for_load()
    await callback_query.message.answer(text, reply_markup=reply_markup)


async def show_languages_page_callback(callback_query: types.CallbackQuery,
                                       callback_data: PaginationCallbackData,
                                       user_settings_presenter: UserSettingsPresenter):
    current_page = callback_data.page
    inline_message_id = callback_query.inline_message_id

    text, reply_markup = await user_settings_presenter.get_languages_list_for_load(current_page)
    await callback_query.message.edit_reply_markup(
        reply_markup=reply_markup,
        inline_message_id=inline_message_id
    )


async def confirm_update_language_callback(callback_query: types.CallbackQuery,
                                           callback_data: LanguageCallbackData,
                                           user_settings_presenter: UserSettingsPresenter):
    lang_name = callback_data.lang_name

    text, reply_markup = await user_settings_presenter.confirm_update_language(lang_name)
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)


async def done_update_language_callback(callback_query: types.CallbackQuery, callback_data: LanguageCallbackData,
                                        user_settings_presenter: UserSettingsPresenter):
    lang_name = callback_data.lang_name

    text = await user_settings_presenter.set_user_language(lang_name)
    await callback_query.message.edit_text(text)


def register_handlers(dp: Dispatcher):
    handlers = [
        (show_languages_callback, LanguageCallbackData.filter(F.action == LanguageCallbackData.Action.UPDATE)),
        (show_languages_page_callback, PaginationCallbackData.filter(F.action == PaginationCallbackData.Action.LANGUAGES)),
        (confirm_update_language_callback, LanguageCallbackData.filter(F.action == LanguageCallbackData.Action.UPDATE_CONFIRM)),
        (done_update_language_callback, LanguageCallbackData.filter(F.action == LanguageCallbackData.Action.UPDATE_DONE))
    ]

    for callback, filter_ in handlers:
        dp.callback_query.register(callback, filter_)
