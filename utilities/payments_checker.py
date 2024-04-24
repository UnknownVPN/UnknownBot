from enums.app import app
from services.crud.db_service import dbService
from services.unknown_api.api_services import Api_Request_handler
from services.nowpayment_api.api_now_pay import NowPaymentHandler
from utilities.CreateNewVpnServices import CreateService
from enums.menu_keyboards import *
from utilities.config_handler import *
import asyncio
from enums.prices import prices


db = dbService()
unknownApi = Api_Request_handler()
nowApi = NowPaymentHandler()
cohandler = ConfigHandler()


connections = {}


async def arzpyment_checker(pay):
    try:
        paystatus = await nowApi.PaymentStatus(pay["payment_id"])
        if paystatus:
            if paystatus["payment_status"] == "finished" and paystatus["status"] == "pending":
                await db.updatePaymentStatus(pay["_id"], "Done")
                if "BuyService" in pay["detail"]:
                    _, server_id, user_count, size, CHtime = pay["detail"].split("_")
                    await CreateService(
                        server_id, int(CHtime), int(size), int(user_count), app, pay
                    )
                elif "ADD_BALANCE" in pay["detail"]:
                    await app.send_message(
                        pay["user_id"],
                        SUCCESSFULL_ADD_BALANCE.format(pay["payment_id"]),
                    )
                    await db.inc_user_amount(pay["user_id"], int(pay["amount"]))
            elif paystatus["payment_status"] == "refunded":
                await app.send_message(
                    pay["user_id"], TRANSACTION_REFUNDED_TEXT.format(pay["payment_id"])
                )
                await db.updatePaymentStatus(pay["_id"], "refunded")

            elif paystatus["payment_status"] == "partially_paid":
                await app.send_message(
                    pay["user_id"], TRANSACTION_PARTIALLY_PAID.format(pay["payment_id"])
                )
                await db.updatePaymentStatus(pay["_id"], "partially_paid")

            elif paystatus["payment_status"] == "failed":
                await app.send_message(
                    pay["user_id"], TRANSACTION_FAILED_TEXT.format(pay["payment_id"])
                )
                await db.updatePaymentStatus(pay["_id"], "failed")

            elif paystatus["payment_status"] == "expired":
                await app.send_message(
                    pay["user_id"], EXPIRED_MESSAGE_CRYPTO.format(pay["payment_id"])
                )
                isupdate = await db.updatePaymentStatus(pay["_id"], "expired")
                logger(__name__).info(isupdate)

            elif paystatus["payment_status"] == "confirmed":
                await app.send_message(
                    pay["user_id"], TRANSACTION_RECEIVED_TEXT.format(pay["payment_id"])
                )

    except Exception as ex:
        logger(__name__).error(f"pasync def get_pyment_checker : {ex}")


async def swaphandler(swap, pay):
    if swap["payed"] == 1 and pay["status"] == "pending":
        await db.updatePaymentStatus(pay["_id"], "Done")
        if "BuyService" in pay["detail"]:
            _, server_id, user_count, size, CHtime = pay["detail"].split("_")
            await CreateService(
                server_id, int(CHtime), int(size), int(user_count), app, pay
            )
        elif "ADD_BALANCE" in pay["detail"]:
            await app.send_message(
                pay["user_id"], SUCCESSFULL_ADD_BALANCE.format(pay["payment_id"])
            )
            await db.inc_user_amount(pay["user_id"], int(pay["amount"]))
