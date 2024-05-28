from src.repositories.user_queue_repository import UserQueueRepository


class UserQueueManager:
    def __init__(self):
        self.user_queues = {}

    def get_user_queue_repository(self, user_id) -> UserQueueRepository:
        if user_id not in self.user_queues:
            self.user_queues[user_id] = UserQueueRepository(user_id)
        return self.user_queues[user_id]