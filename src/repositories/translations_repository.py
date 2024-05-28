import math
import os

from natsort import natsorted

from src.config import LOCALES_PATH


class TranslationsRepository:
    def __init__(self):
        self.translations = self._load_translations()

    @staticmethod
    def _load_translations():
        try:
            translations = natsorted(
                d for d in os.listdir(LOCALES_PATH) if os.path.isdir(os.path.join(LOCALES_PATH, d))
            )
            return translations
        except FileNotFoundError:
            return []

    def get_translation_names_all(self):
        return self.translations

    def get_translation_names(self, limit=None, offset=0):
        total_count = len(self.translations)

        start_index = offset
        end_index = offset + limit if limit else None

        translations_page = self.translations[start_index:end_index]
        total_pages = math.ceil(total_count / limit) if limit else 1

        return translations_page, total_pages
