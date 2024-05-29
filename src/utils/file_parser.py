import base64
import magic
import os
from aiogram import Bot
import textract
from textract.exceptions import ExtensionNotSupported

from src.config import GEMINI_SUPPORTED_MIME_TYPES, TEMP_PATH


async def process_file(translator, bot: Bot, file_id):
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    local_file_name = f"{file_id}{file_extension}"
    local_file_path = os.path.join(TEMP_PATH, local_file_name)

    await bot.download_file(file_path, local_file_path)

    mime_detector = magic.Magic(mime=True)
    mime_type = mime_detector.from_file(local_file_path)

    if file_extension.lower() not in GEMINI_SUPPORTED_MIME_TYPES:
        try:
            text = textract.process(local_file_path, encoding='utf-8')
            file_base64 = base64.b64encode(text).decode('utf-8')
            mime_type = "text/plain"
        except ExtensionNotSupported:
            os.remove(local_file_path)
            raise ValueError(translator("unsupported_file_extension", file_extension=file_extension))
        except Exception:
            os.remove(local_file_path)
            raise ValueError(translator("data_extraction_failed"))
    else:
        with open(local_file_path, "rb") as f:
            file_base64 = base64.b64encode(f.read()).decode('utf-8')

    os.remove(local_file_path)
    return {"inline_data": {"data": file_base64, "mime_type": mime_type}}
