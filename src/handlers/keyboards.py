from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.callback_data.chat_editor_callback_data import ChatEditorCallbackData
from src.callback_data.history_callback_data import HistoryCallbackData
from src.callback_data.instruction_callback_data import InstructionCallbackData
from src.callback_data.language_callback_data import LanguageCallbackData
from src.callback_data.pagination_callback_data import PaginationCallbackData
from src.handlers.callbacks.common_callbacks import CancelCallbackData
from src.utils.translator import Translator


def create_pagination_buttons(translator: Translator, current_page, max_page, action):
    buttons = []
    if current_page > 1:
        buttons.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=PaginationCallbackData(
                action=action,
                page=current_page - 1).pack()))
    if max_page > 1:
        buttons.append(InlineKeyboardButton(
            text=f"{current_page} / {max_page}",
            callback_data="no_data"))
    if current_page < max_page:
        buttons.append(InlineKeyboardButton(
            text="➡️",
            callback_data=PaginationCallbackData(
                action=action,
                page=current_page + 1).pack()))
    buttons.append(InlineKeyboardButton(
        text=translator("cancel"),
        callback_data=CancelCallbackData(
            action=CancelCallbackData.Action.DEL_MSG_CLEAR_STATE,
            history_name=None).pack()))
    return buttons


def create_row_sizes(num_menu_buttons, current_page, total_pages, can_cancel=True):
    row_sizes = [1] * num_menu_buttons

    is_edge_page = current_page in {1, total_pages}
    should_append_two = is_edge_page and total_pages > 1

    row_sizes.append(2 if should_append_two else 3)

    if can_cancel:
        row_sizes.append(1)

    return row_sizes


def kb_menu(translator: Translator, current_page: int = 1):
    kb = InlineKeyboardBuilder()
    button_groups = [
        [
            InlineKeyboardButton(text=translator("edit_instruction"),
                                 callback_data=InstructionCallbackData(
                                     action=InstructionCallbackData.Action.UPDATE).pack()),
            InlineKeyboardButton(text=translator("load_history"),
                                 callback_data=HistoryCallbackData(
                                     action=HistoryCallbackData.Action.LOAD,
                                     history_name=None).pack()),
            InlineKeyboardButton(text=translator("clear_history"),
                                 callback_data=HistoryCallbackData(
                                     action=HistoryCallbackData.Action.CLEAR_CONFIRM,
                                     history_name=None).pack()),
            InlineKeyboardButton(text=translator("delete_history"),
                                 callback_data=HistoryCallbackData(
                                     action=HistoryCallbackData.Action.DELETE,
                                     history_name=None).pack())
        ],
        [
            InlineKeyboardButton(text=translator("edit_last_response"),
                                 callback_data=ChatEditorCallbackData(
                                     action=ChatEditorCallbackData.Action.UPDATE_LAST,
                                     history_name=None).pack()),
            InlineKeyboardButton(text=translator("update_language"),
                                 callback_data=LanguageCallbackData(
                                     action=LanguageCallbackData.Action.UPDATE,
                                     lang_name=None).pack())
        ]
    ]

    total_pages = len(button_groups)

    try:
        buttons = button_groups[current_page - 1]
    except IndexError:
        buttons = []

    for button in buttons:
        kb.add(button)

    kb.add(*create_pagination_buttons(translator, current_page, total_pages, PaginationCallbackData.Action.MENU_PAGE))

    row_sizes = create_row_sizes(len(buttons), current_page, total_pages)
    kb.adjust(*row_sizes)

    return kb.as_markup()


def kb_confirm_delete_history(translator: Translator, history_name: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=translator("yes_delete"),
              callback_data=HistoryCallbackData(
                  action=HistoryCallbackData.Action.DELETE_DONE,
                  history_name=history_name).pack())
    kb.button(text=translator("cancel"),
              callback_data=CancelCallbackData(
                  action=CancelCallbackData.Action.DEL_MSG_CLEAR_STATE,
                  history_name=None).pack())
    kb.adjust(2)

    return kb.as_markup()


def kb_confirm_load_history(translator: Translator, history_name):
    kb = InlineKeyboardBuilder()
    kb.button(text=translator("yes_load"),
              callback_data=HistoryCallbackData(
                  action=HistoryCallbackData.Action.LOAD_DONE,
                  history_name=history_name).pack())
    kb.button(text=translator("no"),
              callback_data=CancelCallbackData(
                  action=CancelCallbackData.Action.DEL_MSG).pack())
    kb.adjust(2)

    return kb.as_markup()


def kb_confirm_clear_history(translator: Translator):
    kb = InlineKeyboardBuilder()
    kb.button(text=translator("yes_clear"),
              callback_data=HistoryCallbackData(
                  action=HistoryCallbackData.Action.CLEAR_DONE,
                  history_name=None).pack())
    kb.button(text=translator("no"),
              callback_data=CancelCallbackData(
                  action=CancelCallbackData.Action.DEL_MSG_CLEAR_STATE).pack())
    kb.adjust(2)

    return kb.as_markup()


def kb_cancel_and_delete_msg(translator: Translator):
    kb = InlineKeyboardBuilder()
    kb.button(text=translator.translate("cancel"),
              callback_data=CancelCallbackData(
                  action=CancelCallbackData.Action.DEL_MSG_CLEAR_STATE).pack())

    return kb.as_markup()


def kb_history_for_load(translator: Translator, history_names, total_pages: int = 1, current_page: int = 1):
    kb = InlineKeyboardBuilder()

    for history_name in history_names:
        kb.add(InlineKeyboardButton(text=history_name,
                                    callback_data=HistoryCallbackData(
                                        action=HistoryCallbackData.Action.LOAD_CONFIRM,
                                        history_name=history_name).pack()))

    kb.add(
        *create_pagination_buttons(translator, current_page, total_pages, PaginationCallbackData.Action.HISTORY_LOAD))

    row_sizes = create_row_sizes(len(history_names), current_page, total_pages)
    kb.adjust(*row_sizes)

    return kb.as_markup()


def kb_history_for_delete(translator: Translator, history_names, total_pages: int = 1, current_page: int = 1):
    kb = InlineKeyboardBuilder()

    for history_name in history_names:
        kb.add(InlineKeyboardButton(text=history_name,
                                    callback_data=HistoryCallbackData(
                                        action=HistoryCallbackData.Action.DELETE_CONFIRM,
                                        history_name=history_name).pack()))

    kb.add(
        *create_pagination_buttons(translator, current_page, total_pages, PaginationCallbackData.Action.HISTORY_DELETE))

    row_sizes = create_row_sizes(len(history_names), current_page, total_pages)
    kb.adjust(*row_sizes)

    return kb.as_markup()


def kb_language(translator: Translator, lang_names, total_pages: int = 1, current_page: int = 1):
    kb = InlineKeyboardBuilder()

    for lang_name in lang_names:
        kb.add(InlineKeyboardButton(text=translator(lang_name),
                                    callback_data=LanguageCallbackData(
                                        action=LanguageCallbackData.Action.UPDATE_CONFIRM,
                                        lang_name=lang_name).pack()))

    kb.add(*create_pagination_buttons(translator, current_page, total_pages, PaginationCallbackData.Action.LANGUAGES))

    row_sizes = create_row_sizes(len(lang_names), current_page, total_pages)
    kb.adjust(*row_sizes)

    return kb.as_markup()


def kb_confirm_update_language(translator: Translator, lang_name: str):
    kb = InlineKeyboardBuilder()
    kb.button(text=translator("yes"),
              callback_data=LanguageCallbackData(
                  action=LanguageCallbackData.Action.UPDATE_DONE,
                  lang_name=lang_name).pack())
    kb.button(text=translator("cancel"),
              callback_data=CancelCallbackData(
                  action=CancelCallbackData.Action.DEL_MSG_CLEAR_STATE,
                  history_name=None).pack())
    kb.adjust(2)

    return kb.as_markup()


def kb_show_menu(translator: Translator):
    kb = InlineKeyboardBuilder()
    kb.button(text="❇️ Меню",
              callback_data=PaginationCallbackData(
                  action=PaginationCallbackData.Action.MENU,
                  page=1).pack())

    return kb.as_markup()
