import os
from motor.motor_asyncio import AsyncIOMotorClient
from schema.user import UserDetails
from schema.chat import Thread, MessageLog
from dotenv import load_dotenv

load_dotenv()



class MongoManager:
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("DATABASE_NAME", "medical_db")
        self.client = None
        self.db = None

    async def connect(self):
        if self.client is None:
            print(f"--- Connecting to MongoDB: {self.db_name} ---", flush=True)
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client[self.db_name]

    async def close(self):
        if self.client:
            self.client.close()

    async def save_user(self, user: UserDetails):
        await self.connect()
        await self.db.users.update_one(
            {"user_id": user.user_id},
            {"$set": user.dict()},
            upsert=True
        )

    # --- Thread Management ---

    async def create_thread(self, user_id: str, title: str = "New Conversation"):
        await self.connect()
        new_thread = Thread(title=title)
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$push": {"threads": new_thread.dict()}}
        )
        return new_thread

    async def get_user_threads(self, user_id: str):
        await self.connect()
        user = await self.db.users.find_one({"user_id": user_id}, {"threads": 1})
        return user.get("threads", []) if user else []

    async def delete_thread(self, user_id: str, thread_id: str):
        await self.connect()
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$pull": {"threads": {"thread_id": thread_id}}}
        )

    async def add_message_to_thread(self, user_id: str, thread_id: str, message: MessageLog):
        await self.connect()
        # Update specific thread inside users array
        await self.db.users.update_one(
            {"user_id": user_id, "threads.thread_id": thread_id},
            {"$push": {"threads.$.messages": message.dict(exclude_none=True)}}
        )
        
        # Update thread title if it's the first message from the user
        if message.user and message.user.query:
            words = message.user.query.split()
            title = " ".join(words[:20])
            if len(words) > 20:
                title += "..."
                
            await self.db.users.update_one(
                {"user_id": user_id, "threads.thread_id": thread_id},
                {"$set": {"threads.$.title": title}}
            )

db_manager = MongoManager()
