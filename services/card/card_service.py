import time
from enums.app import app
from services.crud.db_service import dbService
from services.unknown_api.api_services import Api_Request_handler
from enums.menu_keyboards import *
from utilities.config_handler import ConfigHandler, logger
import asyncio, requests
from enums.prices import prices


db = dbService()
unknownApi = Api_Request_handler()
cohandler = ConfigHandler().getconfig()


async def handl_trasection(stop_event):
    while not stop_event.is_set():
        try:
            card_payments = await db.get_all_card_payment()
            if card_payments == None:
                continue

            for transaction in card_payments:
                now = time.time()
                if (transaction["date"] + 3600) < now:
                    await db.updateCardPaymentStatus(transaction["_id"], "expired")
                    try:
                        await app.send_message(
                            transaction["user_id"], EXPIRED_CARD_PAYMENT
                        )
                    except Exception as e:
                        logger(__name__).error(e)
                    continue

                status = await get_transaction_status(
                    transaction["Card_Number"], transaction["amount"]
                )

                if not status:
                    continue

                payment = await db.get_payment(transaction["_id"])
                if payment and "ADD_BALANCE" in payment["detail"]:
                    await db.updatePaymentStatus(transaction["_id"], "Done")
                    await db.updateCardPaymentStatus(transaction["_id"], "Done")
                    await app.send_message(
                        payment["user_id"],
                        SUCCESSFULL_ADD_BALANCE.format(transaction["_id"]),
                    )
                    await db.inc_user_amount(payment["user_id"], transaction["amount"])

                elif "BuyService" in payment["detail"]:
                    _, server_id, user_count, size, CHtime = payment["detail"].split(
                        "_"
                    )
                    BuyStatus = await unknownApi.createService(
                        server_id, int(CHtime), int(size), int(user_count)
                    )
                    if BuyStatus and BuyStatus["status"]:
                        await db.updatePaymentStatus(transaction["_id"], "Done")
                        await db.updateCardPaymentStatus(transaction["_id"], "Done")
                        ServiceInfo = await unknownApi.getApiServiceInfo(
                            BuyStatus["license"]
                        )
                        dir_link = await unknownApi.getservicelinks(
                            BuyStatus["license"]
                        )
                        await db.insertNewVpnService(
                            ServiceInfo["service"]["name"],
                            transaction["user_id"],
                            BuyStatus["license"],
                            ServiceInfo["service"]["server_name"].split(" ")[0],
                            int(size),
                            int(user_count),
                            dir_link=dir_link["direct"],
                        )
                        await app.send_message(
                            payment["user_id"],
                            SUCCESSFULL_BUY.format(
                                transaction["_id"], CHtime, user_count, size
                            ),
                        )

                        user = await db.get_user(payment["user_id"])
                        if user["refferal"]:
                            await db.inc_user_amount(
                                user["refferal"], prices.giftAmount
                            )
                            await app.send_message(
                                user["refferal"],
                                REF_BUY_SUCESSS.format(prices.giftAmount),
                            )

                    else:
                        await db.updatePaymentStatus(transaction["user_id"], "backed")
                        await db.updateCardPaymentStatus(transaction["_id"], "backed")
                        if BuyStatus:
                            if BuyStatus["message"] == "server full":
                                await app.send_message(
                                    payment["user_id"],
                                    BALANCE_EXCEPT_BUY2.format(transaction["_id"]),
                                )
                            elif BuyStatus["message"] == "buy disabled":
                                await app.send_message(
                                    payment["user_id"],
                                    BALANCE_EXCEPT_BUY2.format(transaction["_id"]),
                                )
                            else:
                                await app.send_message(
                                    payment["user_id"],
                                    BALANCE_EXCEPT_BUY3.format(transaction["_id"]),
                                )
                        else:
                            await app.send_message(
                                BALANCE_EXCEPT_BUY3.format(transaction["_id"])
                            )
                        await db.inc_user_amount(
                            transaction["user_id"], payment["amount"]
                        )

            await asyncio.sleep(2 * 60 + 30)
        except Exception as ex:
            logger(__name__).error(ex)
            await asyncio.sleep(4 * 60 + 30)
        await asyncio.sleep(20)
    return


async def get_transaction_status(card: int, amount: int):
    url = cohandler["payment"]["ghoghnoos_gateway"]
    admin_key = cohandler["payment"]["ghoghnoos_admin_key"]

    try:
        data = requests.post(
            f"{url}/checkPayment",
            json={
                "key": admin_key,
                "cardNumber": str(card),
                "amount": str(amount * 10),
            },timeout=5
        ).json()

        if data["status"]:
            logger(__name__).info(f"Payment Success! {card} {amount} {data}")
            return True

        return False

    except Exception as e:
        logger(__name__).error(f"Error in get card request {e}")
        return False


async def get_card():
    url = cohandler["payment"]["ghoghnoos_gateway"]
    admin_key = cohandler["payment"]["ghoghnoos_admin_key"]

    try:
        _request = requests.post(f"{url}/getCards", json={"key": admin_key},timeout=5)
        logger(__name__).info(_request.text)

        data = _request.json()

        if data == []:
            logger(__name__).error(f"Card Not Found {data}!")
            return False, None

        logger(__name__).info(data)
        return True, data[0]

    except Exception as e:
        logger(__name__).error(f"Error in get card request {e}\n{_request.text}")
        return False, None
