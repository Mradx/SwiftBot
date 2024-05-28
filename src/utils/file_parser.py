import base64
import mimetypes
import os

import textract
from textract.exceptions import ExtensionNotSupported

from src.config import GEMINI_SUPPORTED_MIME_TYPES


async def process_file(translator, bot, file_id):
    file = await bot.get_file(file_id)
    file_path = file.file_path

    mime_type, _ = mimetypes.guess_type(file_path)
    _, file_extension = os.path.splitext(file_path)

    file_name = f"{file_id}{file_extension}"
    await bot.download_file(file_path, file_name)

    if file_extension.lower() not in GEMINI_SUPPORTED_MIME_TYPES:
        try:
            text = textract.process(file_name, encoding='utf-8')
            file_base64 = base64.b64encode(text).decode('utf-8')
            mime_type = "text/plain"
        except ExtensionNotSupported:
            os.remove(file_name)
            raise ValueError(translator("unsupported_file_extension", file_extension=file_extension))
        except Exception:
            os.remove(file_name)
            raise ValueError(translator("data_extraction_failed"))
    else:
        with open(file_name, "rb") as f:
            file_base64 = base64.b64encode(f.read()).decode('utf-8')

    os.remove(file_name)
    return {"inline_data": {"data": file_base64, "mime_type": mime_type}}
