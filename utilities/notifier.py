from enums.app import app
from services.crud.db_service import dbService
from services.unknown_api.api_services import Api_Request_handler
from enums.menu_keyboards import *
from utilities.config_handler import *
import asyncio, time
from enums.prices import prices

db = dbService()
unknownApi = Api_Request_handler()
cohandler = ConfigHandler()


connections = {}

_count_to_log = 0

async def notifier(stop_event):
    global _count_to_log
    while not stop_event.is_set():
        Services = await db.get_all_services()
        if _count_to_log == 10:
            logger(__name__).info(f"services: {len(Services)}")
            _count_to_log = 0

        _count_to_log += 1
        for Service in Services:
            if stop_event.is_set():
                break
            try:
                owner = Service["userId"]
                alarm = Service["alarm"]
                auto_pay = Service["autopay"]
                vpnstatus = Service["status"]
                warn85 = Service["warn85"] # remain_size , used_size , users_count
                if vpnstatus == False:
                    continue
                license = Service["license"]
                name = Service["name"]
                service_info = await unknownApi.getApiServiceInfo(license)

                if service_info and service_info["status"]:
                    if alarm:
                        conn = await unknownApi.GetServiceConn(license)
                        if conn and conn["status"]:
                            for i in conn["connections"]:
                                if license in connections.keys():
                                    if i not in connections[license]:
                                        await app.send_message(
                                            owner,
                                            ALERT_CONNECTION_TEXT.format(name, i, i),
                                            disable_web_page_preview=True,
                                        )
                                        connections[license].append(i)
                                else:
                                    connections[license] = [i]
                                    await app.send_message(
                                        owner,
                                        ALERT_CONNECTION_TEXT.format(name, i, i),
                                        disable_web_page_preview=True,
                                    )

                    if auto_pay:
                        size = Service["size"]
                        usercount = Service["user_count"]
                        price = prices.size[usercount][size]
                        if (
                            service_info["service"]["extendable"]
                            and time.time() > service_info["service"]["expiryTime"]
                        ):
                            transStatus = await db.MakeBuyTransection(owner, price)
                            if transStatus:
                                ExteService = await unknownApi.ExteService(
                                    service_info["service"]["id"]
                                )
                                db.updateServiceWarn85(license,False)
                                if ExteService and ExteService["status"]:
                                    await app.send_message(
                                        owner,
                                        SUCCESSFULL_EXTENSION_TEXT.format(
                                            service_info["service"]["name"]
                                        ),
                                    )
                                    continue
                                else:
                                    await db.inc_user_amount(owner, int(price))
                            else:
                                await app.send_message(
                                    owner, NO_BALANCE_FOR_AUTO_PAY_TEXT
                                )
                                await db.SetVpnServiceAutopay(license, False)
                                continue

                    if not warn85:
                        size = Service["size"]
                        size85 = size * 0.85
                        used_size = service_info["service"]["used_size"]
                        if used_size >= size85:
                            db.updateServiceWarn85(license,True)
                            await app.send_message(
                                owner,
                                SERVICE_SIZE_85_TEXT.format(service_info["service"]["name"]),
                                disable_web_page_preview=True,
                            )

            except Exception as ex:
                logger(__name__).error(
                    f'notif error : \n {ex}\n service_id : {Service["license"]}'
                )
        await asyncio.sleep(15)

    return
