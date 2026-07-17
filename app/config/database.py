from pymongo import MongoClient
from app.core.settings import settings

class Database:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URI)
        self.db = self.client[settings.DATABASE_NAME]

    def get_database(self):
        return self.db
    
database = Database()
db = database.get_database()