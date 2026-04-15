import os
from motor.motor_asyncio import AsyncIOMotorClient
from schema.user import UserDetails
from schema.chat import Thread, MessageLog
from dotenv import load_dotenv

load_dotenv()



class MongoManager:
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("DATABASE_NAME")
        self.client = None
        self.db = None

    async def connect(self):
        if self.client is None:
            if not self.uri or not self.db_name:
                print("--- ERROR: MONGODB_URI or DATABASE_NAME not set in environment! ---", flush=True)
                return
                
            print(f"--- Connecting to MongoDB: {self.db_name} ---", flush=True)
            try:
                self.client = AsyncIOMotorClient(self.uri)
                self.db = self.client[self.db_name]
            except Exception as e:
                print(f"--- MONGODB CONNECTION FAILED: {e} ---", flush=True)

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

    async def create_thread(self, user_id: str, title: str = "New Visualizer Story"):
        await self.connect()
        new_thread = Thread(title=title)
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$push": {"threads": new_thread.dict(exclude_none=True)}}
        )
        return new_thread

    async def get_user_threads(self, user_id: str):
        """Returns full threads with all messages (Warning: slow if images are large)."""
        await self.connect()
        user = await self.db.users.find_one({"user_id": user_id}, {"threads": 1})
        return user.get("threads", []) if user else []

    async def get_user_threads_summary(self, user_id: str):
        """Returns only thread metadata (no messages) for fast sidebar loading."""
        await self.connect()
        user = await self.db.users.find_one(
            {"user_id": user_id},
            {"threads.thread_id": 1, "threads.title": 1, "threads.created_at": 1}
        )
        return user.get("threads", []) if user else []

    async def get_thread_by_id(self, user_id: str, thread_id: str):
        """Fetches a single thread including all messages directly from MongoDB."""
        await self.connect()
        user = await self.db.users.find_one(
            {"user_id": user_id, "threads.thread_id": thread_id},
            {"threads.$": 1}
        )
        if user and "threads" in user and len(user["threads"]) > 0:
            return user["threads"][0]
        return None

    async def delete_thread(self, user_id: str, thread_id: str):
        await self.connect()
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$pull": {"threads": {"thread_id": thread_id}}}
        )

    async def add_message_to_thread(self, user_id: str, thread_id: str, message: MessageLog):
        await self.connect()
        # Update thread inside users array
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
