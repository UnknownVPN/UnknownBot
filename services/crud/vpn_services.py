from services.crud.db_handler import MongoDBHandler
from utilities.utils import change_config_name, change_service_name
from enums.datebaseenums import database


class vpnServices(MongoDBHandler):
    def __init__(self):
        super().__init__()
        self.vpnCollectionName = database.vpnServices

    async def get_user_services(self, userId: int):
        query = {"userId": userId}
        return await self.find_all(self.vpnCollectionName, query)

    async def getServiceInfo(self, license):
        query = {"license": license}
        return await self.find(self.vpnCollectionName, query)

    async def insertNewVpnService(
        self,
        name: str,
        userId: int,
        vpnlicense: str,
        flag: str,
        size: int,
        user_count: int,
        status=True,
        dir_link=None,
    ) -> None:
        query = {
            "name": name,
            "license": vpnlicense,
            "userId": userId,
            "flag": flag,
            "alarm": False,
            "autopay": False,
            "size": size,
            "user_count": user_count,
            "status": status,
            "dir_link": change_config_name(dir_link, name, flag),
        }
        return await self.insert(self.vpnCollectionName, query)

    async def updateServiceName(self, license, name):
        query = {
            "license": license,
        }
        update_data = {"$set": {"name": name}}
        await self.update(self.vpnCollectionName, query, update_data)

    async def updateServicelink(self, license, dir_link, name, flag):
        query = {
            "license": license,
        }
        update_data = {"$set": {"dir_link": change_config_name(dir_link, name, flag)}}
        await self.update(self.vpnCollectionName, query, update_data)

    async def updateServiceStatus(self, license, status):
        query = {
            "license": license,
        }
        update_data = {"$set": {"status": status}}
        await self.update(self.vpnCollectionName, query, update_data)

    async def SetVpnServiceAlarm(self, license, alarm=True):
        query = {
            "license": license,
        }
        update_data = {"$set": {"alarm": alarm}}
        await self.update(self.vpnCollectionName, query, update_data)

    async def SetVpnServiceAutopay(self, license, autopay=True):
        query = {
            "license": license,
        }
        update_data = {"$set": {"autopay": autopay}}
        await self.update(self.vpnCollectionName, query, update_data)

    async def get_all_services(self):
        query = {"status": True}
        return await self.find_all(self.vpnCollectionName, query)
