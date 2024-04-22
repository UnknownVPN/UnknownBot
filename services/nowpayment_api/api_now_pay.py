import aiohttp
from enums.now_payment import endpoints
from utilities.config_handler import *

cohandler = ConfigHandler()

api_key = cohandler.config["payment"]["nowpayment_key"]


class NowPaymentHandler:
    def __init__(self) -> None:
        self.url = cohandler.config["payment"]["nowpayments_api_url"]

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


ACCEPTED_COIN_NAMES = {
    "1inch": "1inch",
    "1inchbsc": "1Inch (BSC)",
    "aave": "Aave",
    "ada": "Cardano (ada)",
    "algo": "Algorand (algo)",
    "ape": "ApeCoin",
    "atom": "Cosmos (atom)",
    "avax": "Avalanche",
    "avaxc": "Avalanche (c-chain)",
    "axs": "Axie Infinity (axs)",
    "babydoge": "Baby Doge Coin",
    "bch": "Bitcoin Cash",
    "bnbbsc": "BNB (bsc)",
    "bnbmainnet": "BNB mainnet",
    "btc": "Bitcoin",
    "bttc": "BTT (trc20)",
    "bttcbsc": "BTT (bsc)",
    "busd": "Busd",
    "busdbsc": "Busd (bsc)",
    "c98": "Coin98",
    "cake": "Cake",
    "chr": "Chromia (chr)",
    "chz": "Chiliz (chz)",
    "cro": "Cronos (cro)",
    "dai": "Dai",
    "dash": "Dash",
    "dgb": "DigiByte",
    "doge": "Doge coin",
    "dogecoin": "Doge Coin (bsc)",
    "dot": "Polkadot",
    "egld": "EGLD",
    "etc": "ETC",
    "eth": "Ethereum",
    "ethbsc": "Ethereum (bsc)",
    "feg": "FEG Token",
    "fil": "Filecoin (fil)",
    "flokibsc": "Floki (bsc)",
    "ftmmainnet": "Fantom (ftm)",
    "ftt": "Ftx Token (ftt)",
    "gal": "Project Galaxy (gal)",
    "gas": "NeoGas (gas)",
    "grt": "The Graph (grt)",
    "gusd": "Gemini Dollar (gusd)",
    "hbar": "Hedera (hbar)",
    "ht": "Huobi Token (ht)",
    "iota": "IOTA",
    "iotx": "IoTeX",
    "kishu": "Kishu inu",
    "klay": "Klaytn (klay)",
    "klv": "Klever (klv)",
    "link": "Chainlink (link)",
    "ltc": "Litecoin",
    "luna": "Terra (luna)",
    "mana": "Decentraland (mana)",
    "maticmainnet": "Matic (polygon)",
    "nano": "Nano",
    "near": "Near",
    "neo": "Neo",
    "ocean": "Ocean Protocol",
    "okb": "Okb",
    "omg": "OMG Network",
    "one": "One",
    "ont": "Ontology (ont)",
    "pax": "Paxos",
    "pit": "Pitbull",
    "qtum": "Qtum",
    "raca": "Radio Caca (raca)",
    "rvn": "Ravencoin (rvn)",
    "sand": "The Sandbox (sand)",
    "shibbsc": "Shiba Inu (BSC)",
    "sol": "Solana",
    "sxpmainnet": "Solar Network (sxp)",
    "tfuel": "Theta Fuel (tfuel)",
    "theta": "Theta Network",
    "tomo": "TomoChain",
    "ton": "Toncoin",
    "trx": "Tron (trx)",
    "tusd": "TrueUSD",
    "usdc": "USDC",
    "usdcmatic": "USD Coin (polygon)",
    "usddtrc20": "USDD (trc20)",
    "usdp": "Pax Dollar (usdp)",
    "usdtbsc": "Tether (bsc)",
    "usdtsol": "Tether (sol)",
    "usdttrc20": "Tether (trx)",
    "vet": "Vechain (vet)",
    "waves": "Waves",
    "xem": "Nem (xem)",
    "xlm": "Stellar (xlm)",
    "xmr": "Monero (xmr)",
    "xrp": "Ripple (xrp)",
    "xtz": "Tezos (xtz)",
    "xvg": "Verge (xvg)",
    "zec": "Zcash (zec)",
    "zen": "Horizen (zen)",
    "zil": "Zilliqa (zil)",
}

SOFT_COINS_NAME = {
    "trx": "Tron (trx)",
}
