import json
import os
import math
import time
from natsort import natsorted
from src.config import HISTORY_PATH
from src.utils.secure import secure_filename

DEFAULT_HISTORY_NAME = "default"
DEFAULT_HISTORY_FILENAME = f"{DEFAULT_HISTORY_NAME}.json"


class UserHistoryRepository:
    def __init__(self, user_id: int, user_name: str = None):
        self.__user_id = user_id
        self.__user_name = user_name
        self.__user_dir = self._get_user_history_dir()

    def _get_user_history_dir(self):
        if not os.path.exists(HISTORY_PATH):
            os.makedirs(HISTORY_PATH)
        user_dir = os.path.join(HISTORY_PATH, str(self.__user_id))
        os.makedirs(user_dir, exist_ok=True)

        return user_dir

    def get_histories(self):
        histories = {}
        for filename in os.listdir(self.__user_dir):
            if filename.endswith(".json") and filename != DEFAULT_HISTORY_FILENAME:
                history_name = filename[:-5]
                with open(os.path.join(self.__user_dir, filename), "r", encoding="utf-8") as f:
                    histories[history_name] = json.load(f)

        return histories

    def get_history_names_all(self):
        history_filenames = natsorted(
            f for f in os.listdir(self.__user_dir) if f.endswith(".json") and f != DEFAULT_HISTORY_FILENAME)
        history_names = [f[:-5] for f in history_filenames]

        return history_names

    def get_history_names(self, limit=None, offset=0):
        history_filenames = natsorted(
            f for f in os.listdir(self.__user_dir) if f.endswith(".json") and f != DEFAULT_HISTORY_FILENAME)
        total_count = len(history_filenames)

        start_index = offset
        end_index = offset + limit if limit else None

        history_names = [f[:-5] for f in history_filenames[start_index:end_index]]
        total_pages = math.ceil(total_count / limit) if limit else 1

        return history_names, total_pages

    def load_history(self, history_name=DEFAULT_HISTORY_NAME):
        history_name = secure_filename(history_name)

        try:
            with open(os.path.join(self.__user_dir, f"{history_name}.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                if history_name != DEFAULT_HISTORY_NAME:
                    self.save_history(data["history"].copy(), data.get("system_instruction"))

                return data["history"], data.get("system_instruction")
        except FileNotFoundError:
            return [], None

    def save_history(self, history=None, system_instruction=None, history_name=DEFAULT_HISTORY_NAME) -> str:
        if history is None and system_instruction is None:
            history, system_instruction = self.load_history()

        data = {
            "history": history,
            "system_instruction": system_instruction
        }

        history_name = secure_filename(history_name)
        with open(os.path.join(self.__user_dir, f"{history_name}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return history_name

    def delete_history(self, history_name: str) -> None:
        history_name = secure_filename(history_name)
        file_path = os.path.join(self.__user_dir, f"{history_name}.json")
        if os.path.exists(file_path):
            os.remove(file_path)

    def add_message(self, role, text):
        history, system_instruction = self.load_history()

        if role == "user":
            meta = f"[user_id={self.__user_id}, current_time={time.strftime('%Y-%m-%d %H:%M:%S %A', time.localtime())} {time.tzname[0]}]"
            text.append(meta)
        history.append({"role": role, "parts": text})

        self.save_history(history, system_instruction)

    def has_previous_model_response(self) -> bool:
        history, _ = self.load_history()
        return bool(history) and history[-1]["role"] == "model"

    def update_last_response(self, new_response):
        history, _ = self.load_history()
        history[-1]["parts"] = [new_response]
        self.save_history(history)

    def get_system_instruction(self, history_name=DEFAULT_HISTORY_NAME):
        _, system_instruction = self.load_history(history_name)
        return system_instruction

    def set_system_instruction(self, instruction):
        history, _ = self.load_history()
        self.save_history(history, instruction)

    def clear_history(self):
        file_path = os.path.join(self.__user_dir, DEFAULT_HISTORY_FILENAME)
        if os.path.exists(file_path):
            os.remove(file_path)
