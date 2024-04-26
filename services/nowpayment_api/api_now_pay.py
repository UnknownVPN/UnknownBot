import aiohttp
from enums.now_payment import endpoints
from utilities.config_handler import *

cohandler = ConfigHandler()

api_key = cohandler.getconfig["payment"]["nowpayment_key"]


class NowPaymentHandler:
    def __init__(self) -> None:
        self.url = cohandler.getconfig["payment"]["nowpayments_api_url"]

    async def send_requets(self, url, payload, headers):
        async with aiohttp.ClientSession() as session:
            try:
                respons = await session.get(
                    url, data=payload, headers=headers, timeout=5
                )
                return await respons.json()
            except Exception as ex:
                logger(__name__).error(f"getting {url} faild error : \n {ex}")
                return None

    async def sendPostRequests(self, url, payload, headers):
        async with aiohttp.ClientSession() as session:
            try:
                respons = await session.post(
                    url, data=payload, headers=headers, timeout=5
                )
                return await respons.json()
            except Exception as ex:
                logger(__name__).error(f"posting {url} faild error : \n {ex}")
                return None

    async def CreatePayment(self, coin: str, price: float, description: str):
        url = f"{self.url}/{endpoints.payment}"
        headers = {"x-api-key": api_key}
        payload = {
            "price_amount": float(price),
            "price_currency": "usd",
            "pay_currency": coin,
            "ipn_callback_url": "https://nowpayments.io",
            "order_description": description,
        }
        return await self.sendPostRequests(url, payload, headers)

    async def fullCurrenscies(self):
        url = f"{self.url}/{endpoints.curreciesList}"
        headers = ({"x-api-key": api_key},)
        payload = {}
        return await self.send_requets(url, payload, headers)

    async def PaymentStatus(self, payment_id):
        url = f"{self.url}/{endpoints.payment}/{payment_id}"
        headers = {"x-api-key": api_key}
        payload = {}
        return await self.send_requets(url, payload, headers)

    async def GetDollarPrice(self):
        url = f"{endpoints.GetDollarPrice}"
        headers = {"x-device-token": "585240a9-2cbc-4c1f-98fe-e7b6a91782cf"}
        payload = {}
        res = await self.send_requets(url, payload, headers)
        return round(float(res["data"]["toman"]), 2)


SOFT_COINS_NAME = {
    "trx": "Tron (trx)",
}
