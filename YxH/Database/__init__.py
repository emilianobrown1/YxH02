from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

mongo = MongoClient(MONGO_DB_URI)
db = mongo.SPL
