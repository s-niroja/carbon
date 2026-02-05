from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://sniroja282005_db_user:OSoyvNtIqjQlvUEE@cluster0.tr3blfp.mongodb.net/"

client = AsyncIOMotorClient(MONGO_URL)

database = client.carbon
users_collection = database.users
history_collection = database.history

def create_unique_index():
 users_collection.create_index("phone",unique=True)

