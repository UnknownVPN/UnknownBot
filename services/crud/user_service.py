from services.crud.db_handler import MongoDBHandler

from enums.datebaseenums import database


class User(MongoDBHandler):
    def __init__(self):
        super().__init__()
        self.userCollectionName = database.usersCollection

    async def get_user(self, id: int):
        query = {"_id": id}
        user = await self.find(self.userCollectionName, query)
        return user

    async def sub_user_amount(self, user_id: int, amount: int):
        query = {"_id": user_id, "balance": {"$gte": amount}}
        update_data = {"$inc": {"balance": -amount}}

        return await self.update(self.userCollectionName, query, update_data)

    async def inc_user_amount(self, user_id: int, amount: int):
        query = {
            "_id": user_id,
        }
        update_data = {"$inc": {"balance": amount}}

        return await self.update(self.userCollectionName, query, update_data)

    async def updateUserStep(self, userId, step):
        query = {"_id": userId}
        update_data = {"$set": {"step": step}}
        return await self.update(self.userCollectionName, query, update_data)

    async def insertNewUser(
        self, id: int, step: str, status="member", refferal=None
    ) -> None:
        query = {
            "_id": id,
            "step": step,
            "status": status,
            "balance": 0,
            "refferal": refferal,
        }

        return await self.insert(self.userCollectionName, query)

    async def get_all_users(self):
        query = {}
        return await self.find_all(self.userCollectionName, query)

    async def get_user_refferals(self, userId: int):
        query = {"refferal": userId}
        return await self.find_all(self.userCollectionName, query)
