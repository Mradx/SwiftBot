import ast
import json
import os

from flake8_plugin_utils import Plugin, Visitor, Error

LOCALES_DIR = './assets/locales'


def parse_string_literal(node):
    if isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return node.value
    return None


class MyError(Error):
    code = 'TC001'
    message = 'Translation key "{key}" not found in translation file for language "{lang}".'


class TranslationKeyVisitor(Visitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translations = self.load_translations()

    def load_translations(self):
        translations = {}
        for lang in os.listdir(LOCALES_DIR):
            lang_dir = os.path.join(LOCALES_DIR, lang)
            if os.path.isdir(lang_dir):
                messages_file = os.path.join(lang_dir, 'strings.json')
                if os.path.isfile(messages_file):
                    with open(messages_file, 'r', encoding='utf-8') as file:
                        translations[lang] = json.load(file)
        return translations

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'translator':
            if len(node.args) > 0:
                key = parse_string_literal(node.args[0])
                if key:
                    for lang, messages in self.translations.items():
                        if key not in messages:
                            self.error_from_node(MyError, node, key=key, lang=lang)

        self.generic_visit(node)


class TranslationCheckerPlugin(Plugin):
    name = 'translation_checker'
    version = '1'
    visitors = [TranslationKeyVisitor]
