import motor.motor_asyncio
from enums.datebaseenums import database
import logging


class MongoDBHandler:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(database.databaseUrl)
        self.db = self.client[database.dateBaseName]

    async def get_user_count(self):
        collection = self.db[database.usersCollection]

        # Get the document count
        count = await collection.count_documents({})
        return count

    async def read(self, collection_name):
        collection = self.db[collection_name]
        documents = []
        async for document in collection.find():
            documents.append(document)
        return documents

    async def find_all(self, collection_name, query):
        collection = self.db[collection_name]
        documents = await collection.find(query).to_list(length=None)
        return documents

    async def find(self, collection_name, query):
        collection = self.db[collection_name]
        document = await collection.find_one(query)
        return document

    async def insert(self, collection_name, query):
        collection = self.db[collection_name]
        try:
            return await collection.insert_one(query)
        except Exception as ex:
            logging.error(
                f"inserting error occurred collection_name : {collection_name} \n {ex}"
            )
            return False

    async def update(self, collection_name, query, update_data):
        collection = self.db[collection_name]
        try:
            await collection.update_one(query, update_data)
            return True
        except Exception as ex:
            logging.error(
                f"update error occurred collection_name : {collection_name} \n {ex}"
            )
            return False

    async def delete(self, collection_name, query):
        collection = self.db[collection_name]
        try:
            await collection.delete_one(query)
            return True
        except Exception as ex:
            logging.error(
                f"delete error occurred collection_name : {collection_name} \n {ex}"
            )
            return False

        # Update user's amount in the database
