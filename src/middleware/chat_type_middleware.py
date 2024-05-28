import logging
from typing import Callable, Dict, Any, Awaitable, Optional

from aiogram import BaseMiddleware, types
from aiogram.enums import ChatType


class ChatTypeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.Update, Dict[str, Any]], Awaitable[Any]],
            event: types.Update,
            data: Dict[str, Any],
    ) -> Any:
        chat_type = self.get_chat_type(event)
        if chat_type is not None and chat_type != ChatType.PRIVATE:
            user = getattr(event, event.event_type).from_user
            logging.info(f"Ignoring non-private message from user {user.id}")
            return

        return await handler(event, data)

    @staticmethod
    def get_chat_type(event: types.Update) -> Optional[ChatType]:
        if event.event_type == 'message':
            return ChatType(event.message.chat.type)
        elif event.event_type == 'callback_query':
            if event.callback_query.message:
                return ChatType(event.callback_query.message.chat.type)
        return None
