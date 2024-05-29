from collections import deque

from src.config import MAX_MESSAGE_TASKS


class UserQueue:
    def __init__(self):
        self.__queue = deque()
        self.__processing_task = None
        self.__error_message_id = None

    def get_queue(self):
        return self.__queue

    def clear_queue(self):
        self.__queue.clear()

    def add_task(self, task):
        if len(self.__queue) < MAX_MESSAGE_TASKS:
            self.__queue.append(task)

    def get_processing_task(self):
        return self.__processing_task

    def set_processing_task(self, task):
        self.__processing_task = task

    def cancel_processing_task(self):
        if self.__processing_task:
            self.__processing_task.cancel()
            self.__processing_task = None

    def get_error_message_id(self):
        return self.__error_message_id

    def set_error_message_id(self, message_id):
        self.__error_message_id = message_id

    def is_queue_full(self):
        return len(self.__queue) >= MAX_MESSAGE_TASKS
