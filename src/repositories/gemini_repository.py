import logging
import random
import google.generativeai as genai
from google.api_core.exceptions import InvalidArgument
from src.config import (
    GEMINI_API_KEYS, GEMINI_MODEL, GEMINI_GENERATION_CONFIG, GEMINI_SAFETY_SETTINGS,
    GEMINI_DEFAULT_SYSTEM_INSTRUCTIONS, GEMINI_SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
)


class GeminiRepository:
    def __init__(self):
        self.__model_name = GEMINI_MODEL

    def _get_model(self, user_system_instruction=None, user_language=None):
        system_instruction = GEMINI_DEFAULT_SYSTEM_INSTRUCTIONS[:]

        if user_system_instruction:
            system_instruction.append(user_system_instruction)

        if user_language:
            language = user_language if user_language in GEMINI_SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
            system_instruction.append(
                f"Provide the answers in this language '{language}' unless the user requests otherwise.")

        while True:
            api_key = random.choice(GEMINI_API_KEYS)
            genai.configure(api_key=api_key)
            try:
                model = genai.GenerativeModel(
                    model_name=self.__model_name,
                    generation_config=GEMINI_GENERATION_CONFIG,
                    system_instruction=system_instruction,
                    safety_settings=GEMINI_SAFETY_SETTINGS
                )
                return model

            except InvalidArgument:
                logging.error(f"Error: invalid API key '{api_key}'. Retrying with a different key...")

    async def count_tokens(self, data) -> int:
        result = await self._get_model().count_tokens_async(data)
        return result.total_tokens

    async def generate_content(self, history, system_instruction, user_inputs: list, user_language: str):
        content = history
        for user_input in user_inputs:
            content += [{"role": "user", "parts": user_input}]

        return await self._get_model(system_instruction, user_language).generate_content_async(content)
