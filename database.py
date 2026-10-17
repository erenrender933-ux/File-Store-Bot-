from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from config import DB_URI, DB_NAME, AUTO_DELETE_TIME


class Database:
    def __init__(self, uri, name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[name]
        self.users = self.db.users
        self.fsub = self.db.fsub
        self.requests = self.db.join_requests
        self.settings = self.db.settings
        self.goals = self.db.goals

    # ---------- users ----------
    async def add_user(self, user_id):
        await self.users.update_one({"_id": user_id}, {"$set": {"active": True}}, upsert=True)

    async def total_users(self):
        return await self.users.count_documents({})

    async def all_users(self):
        return [u["_id"] async for u in self.users.find({})]

    async def del_user(self, user_id):
        await self.users.delete_one({"_id": user_id})

    # ---------- force sub channels ----------
    async def add_fsub(self, chat_id, title, link, request=False):
        await self.fsub.update_one(
            {"_id": chat_id},
            {"$set": {"title": title, "link": link, "request": request}},
            upsert=True,
        )

    async def del_fsub(self, chat_id):
        await self.fsub.delete_one({"_id": chat_id})
        await self.goals.delete_one({"_id": chat_id})

    async def clear_fsub(self):
        await self.fsub.delete_many({})
        await self.goals.delete_many({})

    async def get_fsubs(self):
        return [c async for c in self.fsub.find({})]

    async def is_fsub(self, chat_id):
        return await self.fsub.find_one({"_id": chat_id}) is not None

    # ---------- join requests ----------
    async def add_request(self, chat_id, user_id):
        """Returns True if this is a NEW request."""
        res = await self.requests.update_one(
            {"_id": f"{chat_id}:{user_id}"}, {"$set": {"ok": True}}, upsert=True
        )
        return res.upserted_id is not None

    async def has_request(self, chat_id, user_id):
        return await self.requests.find_one({"_id": f"{chat_id}:{user_id}"}) is not None

    # ---------- request goals ----------
    async def set_goal(self, chat_id, goal):
        await self.goals.update_one(
            {"_id": chat_id},
            {"$set": {"goal": goal, "count": 0, "done": False}},
            upsert=True,
        )

    async def del_goal(self, chat_id):
        await self.goals.delete_one({"_id": chat_id})

    async def get_goals(self):
        return [g async for g in self.goals.find({})]

    async def bump_goal(self, chat_id):
        """Add 1 to goal counter. Returns goal doc only when goal just completed."""
        g = await self.goals.find_one_and_update(
            {"_id": chat_id, "done": False},
            {"$inc": {"count": 1}},
            return_document=ReturnDocument.AFTER,
        )
        if g and g["count"] >= g["goal"]:
            await self.goals.update_one({"_id": chat_id}, {"$set": {"done": True}})
            return g
        return None

    # ---------- settings ----------
    async def get_delete_time(self):
        d = await self.settings.find_one({"_id": "delete_time"})
        return d["value"] if d else AUTO_DELETE_TIME

    async def set_delete_time(self, seconds):
        await self.settings.update_one(
            {"_id": "delete_time"}, {"$set": {"value": seconds}}, upsert=True
        )


db = Database(DB_URI, DB_NAME)
