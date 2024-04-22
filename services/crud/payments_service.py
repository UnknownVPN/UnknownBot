from services.crud.db_handler import *
from enums.datebaseenums import database
from bson.objectid import ObjectId
from datetime import datetime, date
import time, re


class Payment(MongoDBHandler):
    def __init__(self):
        super().__init__()
        self.handler = MongoDBHandler()
        self.payCollectionName = database.payments

    async def updatePaymentStatus(self, id, status):
        query = {"_id": ObjectId(id)}
        update_data = {"$set": {"status": status}}
        return await self.update(self.payCollectionName, query, update_data)

    async def updatePayment_Id(self, id, payment_id):
        query = {"_id": ObjectId(id)}
        update_data = {"$set": {"payment_id": payment_id}}
        await self.update(self.payCollectionName, query, update_data)

    async def insertPayments(
        self, user_id: int, amount: int, status="pending", detail=None, payment_id=None
    ):
        dt = time.time()
        query = {
            "payment_id": payment_id,
            "user_id": user_id,
            "amount": amount,
            "detail": detail,
            "status": status,
            "date": dt,
        }
        return await self.insert(self.payCollectionName, query)

    async def get_today_payment(self):
        current_unix_time = int(time.time())
        start_of_day_unix_time = current_unix_time - (current_unix_time % 86400)
        end_of_day_unix_time = start_of_day_unix_time + 86400
        regex = re.compile(r"BuyService", re.IGNORECASE)
        query = {
            "date": {"$gte": start_of_day_unix_time, "$lte": end_of_day_unix_time},
            "detail": {"$regex": regex},
            "status": "Done",
        }
        # Fetch all payments made today
        return await self.find_all(self.payCollectionName, query)

    async def get_all_buy_payment(self):
        regex = re.compile(r"BuyService", re.IGNORECASE)
        # Create a query for documents with the current date
        query = {"detail": {"$regex": regex}, "status": "Done"}
        # Fetch all payments made today
        return await self.find_all(self.payCollectionName, query)

    async def GetPendingPayments(self):
        return await self.find_all(self.payCollectionName, {"status": "pending"})

    async def get_user_payments(self, user_id: int):
        regex = re.compile(r"BuyService", re.IGNORECASE)
        query = {
            "user_id": user_id,
            "detail": {"$regex": regex},
            "status": "Done",
        }
        userPayments = await self.find_all(self.payCollectionName, query)
        return userPayments

    async def get_payment(self, id: str):
        query = {"_id": ObjectId(id)}
        return await self.find(self.payCollectionName, query)

    async def get_buy_payment_id(self, id: str):
        query = {"payment_id": id}
        return await self.find(self.payCollectionName, query)
