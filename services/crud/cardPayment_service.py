from services.crud.db_handler import *
from enums.datebaseenums import database
from bson.objectid import ObjectId
import time
import pytz


class CardPayment(MongoDBHandler):
    def __init__(self):
        super().__init__()
        self.handler = MongoDBHandler()
        self.CardpayCollectionName = database.Cardpayments

    async def updateCardPaymentStatus(self, payment_id, status):
        query = {"_id": payment_id}
        update_data = {"$set": {"status": status}}
        await self.update(self.CardpayCollectionName, query, update_data)

    async def insertCardPayments(
        self,
        user_id: int,
        Card_Number: int,
        amount: int,
        status="pending",
        payment_id=None,
    ):
        dt = time.time()
        query = {
            "_id": payment_id,
            "Card_Number": Card_Number,
            "amount": amount,
            "status": status,
            "user_id": user_id,
            "date": dt,
        }
        return await self.insert(self.CardpayCollectionName, query)

    async def get_all_card_payment(self):
        # Create a query for documents with the current date
        query = {"status": "pending"}
        # Fetch all payments made today
        return await self.find_all(self.CardpayCollectionName, query)

    async def get_user_card_payments(self, user_id: int):
        query = {"user_id": user_id}
        userPayments = await self.find_all(self.CardpayCollectionName, query)
        return userPayments

    async def get_card_payment(self, id: str):
        query = {"_id": ObjectId(id)}
        return await self.find(self.CardpayCollectionName, query)

    async def getCardPayment(self, Card_Number: int, amount: int):
        query = {"status": "pending", "Card_Number": Card_Number, "amount": amount}
        return await self.find(self.CardpayCollectionName, query)

    async def get_card_pending(self, card_number: int):
        query = {"Card_Number": card_number}
        data = await self.find_all(self.CardpayCollectionName, query)
        return data
