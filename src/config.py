import os

from dotenv import load_dotenv

load_dotenv()

# Proxy
USE_PROXY = False
PROXY = os.environ.get('PROXY')

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
HISTORY_PATH = "data/history"
LOCALES_PATH = "assets/locales"
IMAGES_PATH = "assets/images"
TEMP_PATH = "temp"
DEFAULT_LANGUAGE = "en"
PAGINATION_LIMIT = 5
RESPONSE_DELAY = 2

# MongoDB
MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DB_NAME = "telegram_bot"

# Gemini
GEMINI_MODEL = "gemini-1.5-pro-latest"
GEMINI_API_KEYS = os.getenv("GEMINI_API_KEYS").split(",")

GEMINI_GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

GEMINI_SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

GEMINI_DEFAULT_SYSTEM_INSTRUCTIONS = [""]

GEMINI_SUPPORTED_MIME_TYPES = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
    '.mp3': 'audio/mpeg',
    '.oga': 'audio/oga',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.flac': 'audio/flac',
    '.txt': 'text/plain'
}
