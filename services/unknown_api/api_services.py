import aiohttp
from enums.unknown_api_end_point import endpoints
import logging, json, time
from utilities.config_handler import *
import asyncio

cohandler = ConfigHandler()


class Api_Request_handler:
    def __init__(self) -> None:
        self.url = cohandler.getconfig["payment"]["unknow_api_url"]

    async def send_requets(self, url, payload, headers, tries=5):
        async with aiohttp.ClientSession() as session:
            try:
                respons = await session.get(
                    url, data=payload, headers=headers, timeout=5
                )
                return await respons.json()

            except Exception as ex:
                if tries == 0:
                    logging.error(f"getting {url} faild error : \n {ex}")
                    return None
                await asyncio.sleep(4)
                return await self.send_requets(url, payload, headers, tries=5)

    async def sendPostRequests(self, url, payload, headers):
        async with aiohttp.ClientSession() as session:
            try:
                respons = await session.post(
                    url, data=payload, headers=headers, timeout=5
                )
                return await respons.json()
            except Exception as ex:
                logging.error(f"posting {url} faild error : \n {ex}")
                return None

    async def GetPrices(self):
        url = f"{self.url}/{endpoints.GetPrices}"
        payload = {}
        headers = {"X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"]}
        return await self.send_requets(url, payload, headers)

    async def GetServers(self):
        url = f"{self.url}/{endpoints.GetServers}"
        payload = {}
        headers = {"X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"]}
        return await self.send_requets(url, payload, headers)

    async def ChangeServiceProtocol(self, license: str, protocol):
        url = f"{self.url}/{endpoints.Changeprotocol}"
        payload = (
            """{
            "protocol":"%s"
            }"""
            % protocol
        )
        headers = {"Authorization": license}
        return await self.sendPostRequests(url, payload, headers)

    async def getservicelinks(self, license: str):
        url = f"{self.url}/{endpoints.GetLinks}"
        payload = {}
        headers = {"Authorization": license}
        return await self.send_requets(url, payload, headers)

    async def buyMoreTraffic(self, service_id: str, size: int):
        url = f"{self.url}/{endpoints.Buymoretraffic}"
        payload = json.dumps({"service_id": service_id, "size": size})
        headers = {
            "X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"],
            "Content-Type": "application/json",
        }
        return await self.sendPostRequests(url, payload, headers)

    async def getApiServiceInfo(self, license: str):
        url = f"{self.url}/{endpoints.GetServiceInfo}"
        payload = {}
        headers = {"Authorization": license}
        status = await self.send_requets(url, payload, headers)
        return status

    async def ChangeServiceName(self, serviceId, name):
        url = f"{self.url}/{endpoints.ChangeName}"
        payload = json.dumps({"service_id": serviceId, "name": name})
        headers = {
            "X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"],
            "Content-Type": "application/json",
        }

        return await self.sendPostRequests(url, payload, headers)

    async def AddUser(self, serviceId: str, count_users: int):
        url = f"{self.url}/{endpoints.BuyMoreUser}"
        payload = {"service_id": serviceId, "count_users": count_users}
        headers = {
            "X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"],
            "Content-Type": "application/json",
        }

        return await self.send_requets(url, payload, headers)

    async def ChangeLink(self, license: str):
        url = f"{self.url}/{endpoints.ChangeLinks}"
        payload = {}
        headers = {"Authorization": license}
        return await self.send_requets(url, payload, headers)

    async def ChangeLocation(self, license: str, server_id: str):
        url = f"{self.url}/{endpoints.Changelocation}"
        payload = '{\r\n    "server_id":"%s"\r\n}' % server_id
        headers = {"Authorization": license}
        return await self.sendPostRequests(url, payload, headers)

    async def GetServiceConn(self, license: str):
        url = f"{self.url}/{endpoints.Getconnections}"
        payload = {}
        headers = {"Authorization": license}
        return await self.send_requets(url, payload, headers)

    async def createService(self, server_id: str, time: int, size: int, count: int):
        url = f"{self.url}/{endpoints.buyservice}"

        headers = {"X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"]}
        payload = (
            '{\r\n    "server_id":"%s",\r\n    "time":"%s",\r\n    "size":"%s",\r\n    "count":"%s"\r\n}'
            % (server_id, time, size, count)
        )
        return await self.sendPostRequests(url, payload, headers)

    async def GetAccInfo(self):
        url = f"{self.url}/{endpoints.AccInfo}"
        payload = {}
        headers = {"X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"]}

        return await self.send_requets(url, payload, headers)

    async def ExteService(self, service_id: str):
        url = f"{self.url}/{endpoints.extensionservice}"
        payload = json.dumps({"service_id": service_id})
        headers = {
            "X-API-KEY": cohandler.getconfig["bot"]["unknow_api_token"],
            "Content-Type": "application/json",
        }
        return await self.send_requets(url, payload, headers)
