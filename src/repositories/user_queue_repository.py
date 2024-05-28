from src.models.queue.user_queue import UserQueue


class UserQueueRepository:
    def __init__(self, user_id: int):
        self.__user_id = user_id
        self.__user_queue = UserQueue()

    def get_queue(self):
        return self.__user_queue.get_queue()

    def clear_queue(self):
        self.__user_queue.clear_queue()

    def add_task(self, task):
        self.__user_queue.add_task(task)

    def get_processing_task(self):
        return self.__user_queue.get_processing_task()

    def set_processing_task(self, task):
        self.__user_queue.set_processing_task(task)

    def cancel_processing_task(self):
        self.__user_queue.cancel_processing_task()

    def get_error_message_id(self):
        return self.__user_queue.get_error_message_id()

    def set_error_message_id(self, message_id):
        self.__user_queue.set_error_message_id(message_id)
