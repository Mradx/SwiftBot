from mongoengine import connect
from src.config import MONGO_URI, MONGO_DB_NAME


class DatabaseManager:
    def __init__(self, uri=MONGO_URI, db_name=MONGO_DB_NAME):
        self.uri = uri
        self.db_name = db_name

    def initialize(self):
        connect(db=self.db_name, host=self.uri)
