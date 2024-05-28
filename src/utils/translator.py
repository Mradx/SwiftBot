import json
import os

from src.config import LOCALES_PATH, DEFAULT_LANGUAGE

STRINGS_FILE = 'strings.json'


class Translator:
    def __init__(self, language):
        self.translations = {}
        self.load_translations()
        if language in self.translations:
            self.language = language
        else:
            self.language = DEFAULT_LANGUAGE

    def load_translations(self):
        for lang in os.listdir(LOCALES_PATH):
            with open(os.path.join(LOCALES_PATH, lang, STRINGS_FILE), 'r', encoding='utf-8') as file:
                self.translations[lang] = json.load(file)

    def translate(self, key, **kwargs):
        translation = self.translations.get(self.language, {}).get(key, key)
        return translation.format(**kwargs)

    def __getattr__(self, key):
        return lambda **kwargs: self.translate(key, **kwargs)

    def __call__(self, key, **kwargs):
        return self.translate(key, **kwargs)
