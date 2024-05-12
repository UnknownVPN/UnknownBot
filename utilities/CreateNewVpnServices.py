from services.crud.db_service import dbService
from services.unknown_api.api_services import Api_Request_handler
from enums.menu_keyboards import *


unknownApi = Api_Request_handler()
db = dbService()


async def CreateService(server_id, CHtime, size, user_count, app, payment):
    BuyStatus = await unknownApi.createService(server_id, CHtime, size, user_count)
    if BuyStatus and BuyStatus["status"]:
        ServiceInfo = await unknownApi.getApiServiceInfo(BuyStatus["license"])
        dir_link = await unknownApi.getservicelinks(BuyStatus["license"])
        await db.insertNewVpnService(
            ServiceInfo["service"]["name"],
            payment["user_id"],
            BuyStatus["license"],
            int(size),
            int(user_count),
            dir_link=dir_link["direct"],
            flag=ServiceInfo["service"]["server_name"].split(" ")[0],
        )
        await app.send_message(
            payment["user_id"],
            SUCCESSFULL_BUY.format(payment["payment_id"], CHtime, user_count, size),
        )
        user = await db.get_user(payment["user_id"])
        if user["refferal"]:
            await db.inc_user_amount(user["refferal"], prices.giftAmount)
            await app.send_message(
                user["refferal"], REF_BUY_SUCESSS.format(prices.giftAmount)
            )
        return ServiceInfo["service"]
    else:
        if BuyStatus:
            if BuyStatus["message"] == "server full":
                await app.send_message(
                    payment["user_id"],
                    BALANCE_EXCEPT_BUY2.format(payment["payment_id"]),
                )
            elif BuyStatus["message"] == "buy disabled":
                await app.send_message(
                    payment["user_id"],
                    BALANCE_EXCEPT_BUY2.format(payment["payment_id"]),
                )
            else:
                await app.send_message(
                    payment["user_id"],
                    BALANCE_EXCEPT_BUY3.format(payment["payment_id"]),
                )
        else:
            await app.send_message(
                payment["user_id"], BALANCE_EXCEPT_BUY3.format(payment["payment_id"])
            )
        await db.inc_user_amount(payment["user_id"], payment["amount"])
        await db.updatePaymentStatus(payment["_id"], "backed")

        return