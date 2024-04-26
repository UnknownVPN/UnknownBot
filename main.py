from utilities.utils import config_domains_check
config_domains_check()

from pyrogram import filters, idle
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from pyrogram.errors.exceptions import FloodWait
from services.crud.db_service import dbService
from services.nowpayment_api.api_now_pay import NowPaymentHandler, SOFT_COINS_NAME
from services.unknown_api.api_services import Api_Request_handler
from jdatetime import datetime as jdate
from datetime import datetime as date
from utilities.config_handler import *
from utilities.custom_filters import *
from utilities import admin_logger
from utilities.CreateNewVpnServices import CreateService
from utilities.card_validation import IsCARD_VALID
from utilities.utils import change_config_name
from utilities import auto_backup
from enums.commands import BotCommands
from enums.menu_keyboards import *
from enums.prices import prices
from threading import Thread
import threading
import io, nest_asyncio
import asyncio
import qrcode
import pytz
from random import choices
from enums.app import app

from utilities.notifier import notifier
from services.card.card_service import handl_trasection, get_card

# initialization pyrogram telegram
nest_asyncio.apply()
cohandler = ConfigHandler()
db = dbService()
unknownApi = Api_Request_handler()
nowapi = NowPaymentHandler()

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@app.on_message(~IsAdmin(app) & is_spamming & ~filters.me)
async def msg_spam_handler(client, message):
    await message.reply(SLOW_DOWN)
    return


@app.on_callback_query(~IsAdmin(app) & is_spamming & ~filters.me)
async def msg_spam_handler(client, query):
    await query.answer(SLOW_DOWN)
    return


@app.on_message(filters.private & BotCommands.start & ~IsAdmin(app) & ~IsJoined(app))
async def member_start_handler(client, message):
    user = await db.get_user(message.chat.id)
    if user == None:
        if message.command[0] == "start" and len(message.command) == 2:
            if (
                message.command[1].isdigit()
                and int(message.command[1]) != message.chat.id
            ):
                await db.insertNewUser(
                    message.chat.id, "Home", "member", int(message.command[1])
                )
        await db.insertNewUser(message.chat.id, "Home", "member")
    await message.reply(
        HELLO_BEFORE_JOIN_TEXT.format(
            message.from_user.first_name, cohandler.config["bot"]["sponsor_channel"]
        ),
        reply_markup=BUTTON_BEFORE_JOIN,
    )

    return


@app.on_message(filters.private & BotCommands.start)
async def member_isjoined_start_handler(client, message):
    user = await db.get_user(message.chat.id)
    if user == None:
        if message.command[0] == "start" and len(message.command) == 2:
            if (
                message.command[1].isdigit()
                and int(message.command[1]) != message.chat.id
            ):
                await db.insertNewUser(
                    message.chat.id, "Home", "member", int(message.command[1])
                )
        await db.insertNewUser(message.chat.id, "Home", "member")
    await message.reply(
        HELLO_TEXT.format(message.from_user.first_name), reply_markup=HELLO_BUTTONS
    )
    return


# joinhandler message handler
@app.on_message(filters.private & ~IsJoined(app) & ~IsAdmin(app))
async def member_join_handler(client, message):
    user = await db.get_user(message.chat.id)
    if user == None:
        await db.insertNewUser(message.chat.id, "Home")
    await message.reply(
        HELLO_BEFORE_JOIN_TEXT.format(message.from_user.first_name),
        reply_markup=BUTTON_BEFORE_JOIN,
    )

    return


# admin message handler
@app.on_message(filters.private & IsAdmin(app) & BotCommands.settings)
async def admin_setting_handler(client, message):
    buystatus = "فعال" if cohandler.config["settings"]["buystatus"] == "True" else "غیر فعال"
    sponsor_channel = (
        "فعال" if cohandler.config["bot"]["sponsor_channel"] != False else "غیر فعال"
    )
    await message.reply(
        BOT_SETTING.format(buystatus, sponsor_channel),
        reply_markup=SETTING_SETUP_BUTTON,
    )
    return

@app.on_message(filters.private & BotCommands.admin_add_balance & IsAdmin(app))
async def admin_add_balance(client, message):
    s = message.text.split(" ")
    user_id = int(s[1])
    amount = int(s[2])
    await db.inc_user_amount(user_id,amount)
    result = await db.get_user(user_id)
    await message.reply(str(result))

@app.on_callback_query(dynamic_data_filter("backtoSettingmanage"))
async def backtoSettingmanage(client, query):
    buystatus = "فعال" if cohandler.config["settings"]["buystatus"] == "True" else "غیر فعال"
    sponsor_channel = (
        "فعال" if cohandler.config["bot"]["sponsor_channel"] != False else "غیر فعال"
    )
    await query.edit_message_text(
        BOT_SETTING.format(buystatus, sponsor_channel),
        reply_markup=SETTING_SETUP_BUTTON,
    )
    return


@app.on_message(filters.private & IsAdmin(app) & BotCommands.admin)
async def admin_start_handler(client, message):
    user = await db.get_user(message.chat.id)
    if user == None:
        await db.insertNewUser(message.chat.id, "Home", status="admin")
    await message.reply(
        ADMIN_HELLO_TEXT.format(message.from_user.first_name),
        reply_markup=ADMIN_MAIN_MENU,
    )
    return


@app.on_message(filters.private & IsAdmin(app) & BotCommands.modeBalance)
async def modeBalance(client, message):
    if message.command[0] == "modbalance" and len(message.command) == 2:
        user = message.command[1].split(":")[0]
        amount = message.command[1].split(":")[1]
        if amount.startswith("-"):
            status = await db.sub_user_amount(int(user), int(amount.replace("-", "")))
        else:
            status = await db.inc_user_amount(int(user), int(amount))

        if status:
            await message.reply("Done")
        else:
            await message.reply(f"failed : {status}")


@app.on_message(filters.private & IsAdmin(app) & BotCommands.statics)
async def statics(client, message):
    info = await unknownApi.GetAccInfo()
    user_count = await db.get_user_count()
    todaypayment = await db.get_today_payment()
    payment = await db.get_all_buy_payment()
    todaybuyamount = 0
    buyamount = 0
    for i in todaypayment:
        todaybuyamount += i["amount"]
    for i in payment:
        buyamount += i["amount"]
    await message.reply(
        f"""
خرید امروز  : {todaybuyamount}
مجموع کل خرید : {buyamount}
تعداد کل سرویس ها : {info['services_count']}
آمار کاربران ربات : {user_count}
موجودی پنل : {info['balance']}
🆔 @"""+cohandler.config["bot"]["sponsor_bot"]
    )


@app.on_message(filters.private & IsAdmin(app) & BotCommands.notification)
async def notification(client, message):
    user_id = message.from_user.id
    await db.updateUserStep(user_id, "Send_PM")
    keyboard = ReplyKeyboardMarkup([["🔙 بازگشت"]], resize_keyboard=True)
    await message.reply(SEND_PM_TEXT, reply_markup=keyboard)


@app.on_message(filters.private & BotCommands.balancetransfer)
async def balanceTransfer(client, message):
    user = await db.get_user(message.chat.id)
    if user != None:
        await message.reply(
            TRANSFER_BALANCE_TEXT.format(user["balance"]),
            reply_markup=CANCEL_TRANSFER_BUTTONS,
        )
        await db.updateUserStep(user["_id"], "TransferBalancValue")
    return


@app.on_message(filters.private & IsAdmin(app))
async def AdminStepHandler(client, message):
    UserId = message.from_user.id
    user = await db.get_user(UserId)
    if user == None:
        await db.insertNewUser(UserId, "Home", "admin")
        user = await db.get_user(UserId)
    userStep = user["step"]
    if userStep == "Send_PM":
        if message.text:
            if message.text == "🔙 بازگشت":
                await message.reply("منوی اصلی", reply_markup=ADMIN_MAIN_MENU)
                await db.updateUserStep(UserId, "Home")
                return
        keyboard = ReplyKeyboardMarkup(
            [["✅ تایید"], ["🔙 بازگشت"]], resize_keyboard=True
        )
        await db.updateUserStep(UserId, f"confirmPM:{message.chat.id}:{message.id}")
        await message.reply(CONFIRM_SEND_PM, reply_markup=keyboard)
        return
    elif userStep.split(":")[0] == "confirmPM":
        if message.text:
            if message.text == "🔙 بازگشت":
                await message.reply(SEND_PM_TEXT, reply_markup=keyboard)
                await db.updateUserStep(UserId, "Send_PM")
                return
            elif message.text == "✅ تایید":
                await db.updateUserStep(UserId, "Home")
                user_all = await db.get_all_users()
                PM_COUNT = 0
                ER_COUNT = 0
                await app.send_message(
                    UserId, "...درحال ارسال", reply_markup=ADMIN_MAIN_MENU
                )
                for i in user_all:
                    try:
                        await app.copy_message(
                            i["_id"],
                            int(userStep.split(":")[1]),
                            int(userStep.split(":")[2]),
                        )
                        PM_COUNT += 1
                        await asyncio.sleep(1)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except Exception as ex:
                        logger(__name__).error("sending message error :{%s}" % ex)
                        ER_COUNT += 1
                        continue
                await app.send_message(
                    UserId,
                    f" پیام ارسال  شد {PM_COUNT} ✅ \nتعداد خطا : {ER_COUNT} ❌",
                    reply_markup=ADMIN_MAIN_MENU,
                )
                return

    elif userStep == "send_channel":
        if message.text:
            if message.text == "🔙 بازگشت":
                await message.reply(
                    CANCEL_ADD_BALANCE_TEXT, reply_markup=ADMIN_MAIN_MENU
                )
                await db.updateUserStep(message.from_user.id, "Home")
                return
            else:
                cohandler.update_config("bot", "sponsor_channel", message.text)
                await message.reply("انجام شد", reply_markup=ADMIN_MAIN_MENU)
                await db.updateUserStep(message.from_user.id, "Home")
                return


@app.on_message(filters.private & BotCommands.emailsubmit)
async def email_handler(client, message):
    await message.reply(THIS_SECTION_DISACTIVATED, reply_markup=HELLO_BUTTONS)
    return


@app.on_message(filters.private & BotCommands.question)
async def question_handler(client, message):
    await message.reply(QUESTIONS_TEXT, reply_markup=QUESTIONS_BUTTONS)
    return


@app.on_message(BotCommands.support)
async def support_handler(client, message):
    await message.reply(SUPPORT_TEXT)
    return


@app.on_message(BotCommands.refferal)
async def get_paid_handler(client, message):
    botid = await app.get_me()
    # TODO get user refferal info
    refferalPayments = 0
    refferalNum = 0
    giftPayed = 0
    userRefferals = await db.get_user_refferals(message.from_user.id)
    if userRefferals:
        for i in userRefferals:
            refferalNum += 1
            refferal = await db.get_user_payments(i["_id"])
            if refferal:
                giftPayed += len(refferal) * prices.giftAmount
                refferalPayments = len(refferal)
    await message.reply(
        REFFERAL_HINT.format(
            botid.username,
            message.from_user.id,
            refferalNum,
            refferalPayments,
            giftPayed,
        )
    )
    return


@app.on_message(BotCommands.Canceltransfer)
async def cancelhandler(client, message):
    user = await db.get_user(message.chat.id)
    await message.reply(CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS)
    await db.updateUserStep(user["_id"], "Home")


@app.on_message(BotCommands.pricese)
async def pricese_handler(client, message):
    await message.reply(PRICE_PRODUCTS_TEXT)
    return


@app.on_message(BotCommands.con_helper)
async def how_connect_handler(client, message):
    await message.reply(HOWCONNECT_TEXT, reply_markup=HOWCONNECT_BUTTONS)
    return


@app.on_message(BotCommands.userServices)
async def user_services(client, message):
    user_services_list = await db.get_user_services(message.from_user.id)
    await db.updateUserStep(message.chat.id, "Home")
    servicebuttons = []
    if user_services_list:
        for services in user_services_list:
            service = await unknownApi.getApiServiceInfo(services["license"])
            if service:
                servicebuttons.append(
                    [
                        InlineKeyboardButton(
                            f"{services['flag']} {services['name']}",
                            callback_data=f"getservice:{services['license']}",
                        )
                    ]
                )
            else:
                await db.updateServiceStatus(services["license"], False)
        servicebuttons.append(
            [InlineKeyboardButton("❌بستن پنل❌", callback_data=f"close")]
        )
        await message.reply(
            MANAGE_SERVICES_TEXT, reply_markup=InlineKeyboardMarkup(servicebuttons)
        )
    else:
        await message.reply(NO_SERVICES_TEXT)
    return


@app.on_message(filters.private & BotCommands.balance)
async def user_balance(client, message):
    user = await db.get_user(message.from_user.id)
    if user:
        await message.reply(
            BALANCE_MESSAGE.format(user["_id"], user["balance"]),
            reply_markup=BALANCE_BUTTONS,
        )
    return


@app.on_message(filters.private & BotCommands.buy_service)
async def Buyservice(client, message):
    status = await unknownApi.GetAccInfo()
    if not status:
        return await message.reply(UNKNOWN_ERROR)

    if not status["status"]:
        logger(__name__).info(status)
        return await apiMsgErrorHandler(status, message)

    if status["balance"] < 500_000:
        await app.send_message(
            cohandler.config["bot"]["admin"],
            "❌ موجودی حساب کمتر از 500 هزار تومن است.\nلطفا موجودی Unknown را شارژ کنید.",
        )
        return await message.reply(
            "⚠️ بخش فروش فعلا در دسترس نمیباشد.\nلطفا با پشتیبانی در ارتباط باشید.\n\n🆔 @"+cohandler.config["bot"]["sponsor_admin"]
        )

    user = await db.get_user(message.from_user.id)
    servers = await unknownApi.GetServers()
    if servers != None:
        server_list = [
            server for server in servers["servers"] if server["enabled"] == True
        ]

        buttons = []

        for row in list(chunks(server_list, 3)):
            row_list = []
            for server in row:
                row_list.append(
                    InlineKeyboardButton(
                        text=server["name"], callback_data=f"Buyservice:{server['id']}"
                    )
                )
            buttons.append(row_list)

        buttons.append([InlineKeyboardButton("❌بستن پنل❌", callback_data=f"close")])
    else:
        await message.reply(UNKNOWN_ERROR)
        return
    if user:
        await message.reply(SERVERS_TEXT, reply_markup=InlineKeyboardMarkup(buttons))
    return


@app.on_message(filters.private & BotCommands.addsize)
async def Addsize(client, message):
    UserId = message.from_user.id
    user_services_list = await db.get_user_services(UserId)
    if user_services_list:
        keyboard = ReplyKeyboardMarkup([["🔙 بازگشت"]], resize_keyboard=True)
        await message.reply(INCREASE_SIZE_TEXT, reply_markup=keyboard)
        await db.updateUserStep(UserId, "addsize")
    else:
        await message.reply(NO_SERVICES_TEXT)
    return


@app.on_message(filters.private & filters.text & ~filters.me)
async def memmberStepHandler(client, message):
    UserId = message.from_user.id
    user = await db.get_user(UserId)
    userStep = user["step"]
    if user == None:
        await message.reply(NOT_REGISTERED_USER_ERROR)
        return
    if userStep == "TransferBalancValue":
        if message.text.isdigit() == False or int(message.text) <= 99:
            await message.reply(INVALID_VALUE_TEXT)
        elif user["balance"] < int(message.text):
            await message.reply(NO_BALANCE_TEXT)
        else:
            await db.updateUserStep(user["_id"], f"TransferBalance:{message.text}")
            await message.reply(TRANSFER_USERID_TEXT.format(message.text))
            return

    elif userStep.split(":")[0] == "Enter_card":
        if message.text == "🔙 بازگشت":
            await message.reply(CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS)
            await db.updateUserStep(message.from_user.id, "Home")
        elif IsCARD_VALID(message.text.replace("-", "").replace(" ", "")):
            await db.updateUserStep(message.from_user.id, "Home")
            payment = await db.get_payment(userStep.split(":")[1])

            _status, data = await get_card()
            if not _status:
                await message.reply(
                    f"{UNKNOWN_ERROR}\n\nلطفا با پشتیبانی در ارتباط باشید!",
                    reply_markup=HELLO_BUTTONS,
                )
                return

            _card = int(message.text.replace("-", "").replace(" ", ""))
            card_in_use = await db.get_card_pending(_card)
            card_in_use = list(filter(lambda x: x["status"] == "pending" and x["user_id"] != UserId,card_in_use)) != []
            if card_in_use:
                await message.reply(CARD_IN_USE,reply_markup=HELLO_BUTTONS)
                return
            
            await message.reply(
                PAY_CARD_TEXT.format(payment["amount"], data["number"], data["name"]),
                reply_markup=HELLO_BUTTONS,
            )
            await db.insertCardPayments(
                UserId,
                _card,
                payment["amount"],
                "pending",
                userStep.split(":")[1],
            )
            return
        else:
            await db.updateUserStep(message.from_user.id, "Home")
            await message.reply(INVALID_CARD_NUMBER)
            return

    elif userStep.split(":")[0] == "TransferBalance":
        if message.text.isdigit():
            userinfo = await db.get_user(int(message.text))
            receiver = userinfo["_id"]
        else:
            try:
                userinfo = await app.get_users(message.text)
                receiver = userinfo.id
            except:
                receiver = None
        if receiver and receiver != UserId:
            await db.updateUserStep(UserId, "Home")
            dt = jdate.now()
            tz = pytz.timezone("Asia/Tehran")
            localized_dt = dt.astimezone(tz)
            date = localized_dt.date().togregorian().isoformat()
            Status = await db.TransferBalance(
                UserId, receiver, int(userStep.split(":")[1])
            )
            if Status:
                await message.reply(
                    COINS_TRANSFERED_TEXT.format(
                        int(userStep.split(":")[1]),
                        date,
                        f"{localized_dt.hour}:{localized_dt.minute}",
                        receiver,
                    ),
                    reply_markup=HELLO_BUTTONS,
                )
                await app.send_message(
                    receiver,
                    ALARM_COINS_RECEIVED_TEXT.format(
                        int(userStep.split(":")[1]),
                        date,
                        f"{localized_dt.hour}:{localized_dt.minute}",
                        UserId,
                    ),
                )

                return
            else:
                await message.reply(UNKNOWN_ERROR, reply_markup=HELLO_BUTTONS)

                return
        else:
            await message.reply(INVALID_USERID_TEXT)
            return

    elif userStep.split(":")[0] == "changename":
        if message.text == "🔙 بازگشت":
            await message.reply("لغو", reply_markup=HELLO_BUTTONS)
            await user_services(client, message)
            await db.updateUserStep(message.from_user.id, "Home")
        else:
            license = userStep.split(":")[1]
            current_info = await unknownApi.getApiServiceInfo(license)
            if current_info:
                status = await unknownApi.ChangeServiceName(
                    current_info["service"]["id"], message.text
                )
                if status and status["status"]:
                    await db.updateUserStep(message.from_user.id, "Home")
                    await db.updateServiceName(license, message.text)
                    dir_link = await unknownApi.getservicelinks(license)
                    await db.updateServicelink(
                        license,
                        dir_link["direct"],
                        message.text,
                        current_info["service"]["server_name"].split(" ")[0],
                    )
                    await message.reply(
                        CHANGED_NAME_SUCCESS_TEXT.format(
                            current_info["service"]["name"], message.text
                        ),
                        reply_markup=HELLO_BUTTONS,
                    )

                    return
                else:
                    await apiMsgErrorHandler(status, message, "name")
            else:
                await apiMsgErrorHandler(current_info, message, "name")

    elif userStep.split(":")[0] == "adduser":
        if message.text == "🔙 بازگشت":
            await message.reply("لغو", reply_markup=HELLO_BUTTONS)
            await user_services(client, message)
            await db.updateUserStep(message.from_user.id, "Home")
        else:
            license = userStep.split(":")[1]
            user = await db.get_user(message.from_user.id)
            if user:
                await message.reply(
                    MORE_USER_FINAL_TEXT.format(
                        message.text, user["balance"], prices.userCount
                    ),
                    reply_markup=MoreUserButton,
                )
                await db.updateUserStep(
                    message.from_user.id, f"addUserFinal:{license}:{message.text}"
                )
                return
            else:
                await message.reply(NOT_REGISTERED_USER_ERROR)
                return

    elif userStep.split(":")[0] == "addUserFinal":
        license = userStep.split(":")[1]
        if message.text == "🔙 بازگشت":
            current_info = await unknownApi.getApiServiceInfo(license)
            if current_info:
                await message.reply(MORE_USER_TEXT, reply_markup=CHANGE_SERVICE_BACK)
                await db.updateUserStep(UserId, f"adduser:{license}")
            else:
                await apiMsgErrorHandler(current_info, message)
                await db.updateUserStep(UserId, f"Home")
                await message.reply("لغو شد", reply_markup=HELLO_BUTTONS)
                return
        elif message.text == "✅ تایید":
            await db.updateUserStep(UserId, "Home")
            await user_services(client, message)
            license = userStep.split(":")[1]
            memberCount = userStep.split(":")[2]

            user = await db.get_user(UserId)
            if user:
                serviceinfo = await unknownApi.getApiServiceInfo(license)
                if serviceinfo == None or serviceinfo["status"] == False:
                    await apiMsgErrorHandler(serviceinfo, message, "moreuser")
                    return
                else:
                    status = await db.MakeBuyTransection(
                        UserId, int(memberCount) * prices.userCount
                    )
                    if status == True:
                        add_user = await unknownApi.AddUser(
                            serviceinfo["service"]["id"], int(memberCount)
                        )
                        if add_user and serviceinfo["status"] == True:
                            await db.insertPayments(
                                UserId,
                                int(memberCount) * prices.userCount,
                                "Done",
                                f"BuyMoreUser_{serviceinfo['service']['id']}_{memberCount}",
                            )
                            await message.reply(
                                SUCCESSFULL_ADD_MORE_USER_TEXT,
                                reply_markup=HELLO_BUTTONS,
                            )
                            return
                        else:
                            await db.inc_user_amount(
                                UserId, int(memberCount) * prices.userCount
                            )
                            await db.insertPayments(
                                UserId,
                                int(memberCount) * prices.userCount,
                                "Done",
                                f"BuyMoreUser_Failed",
                            )
                            await message.reply(
                                ADDMOREUSERFAILED, reply_markup=HELLO_BUTTONS
                            )
                            return

                    else:
                        await message.reply(
                            NO_BALANCE_FOR_MORE_USER, reply_markup=HELLO_BUTTONS
                        )
                        return
            else:
                await message.reply(NOT_REGISTERED_USER_ERROR)
                return

    elif userStep.split(":")[0] == "addsize":
        if message.text == "🔙 بازگشت":
            await message.reply(CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS)
            await db.updateUserStep(UserId, "Home")
            return
        elif (
            message.text.isdigit() == False
            or 600 < int(message.text)
            or int(message.text) < 1
        ):
            await message.reply(INCREASE_SIZE_RANGE_ERROR_TEXT)
            return
        elif message.text.isdigit():
            user_services_list = await db.get_user_services(UserId)
            servicebuttons = []
            if user_services_list:
                for services in user_services_list:
                    servicebuttons.append(
                        [
                            InlineKeyboardButton(
                                f"{services['flag']} {services['name']}",
                                callback_data=f"addsizeto:{services['license']}:{message.text}",
                            )
                        ]
                    )
            else:
                await message.reply(NO_SERVICES_TEXT, reply_markup=HELLO_BUTTONS)

                return
            servicebuttons.append(
                [InlineKeyboardButton("❌بستن پنل❌", callback_data=f"close")]
            )

            await message.reply(
                CHOOSE_SERVICE_ADD_SIZE_TEXT.format(message.text),
                reply_markup=InlineKeyboardMarkup(servicebuttons),
            )

    elif userStep == "addbalance":
        if message.text == "🔙 بازگشت":
            await message.reply(CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS)
            await db.updateUserStep(message.from_user.id, "Home")
        elif message.text.endswith("0") == False or message.text.isdigit() == False:
            keyboard = ReplyKeyboardMarkup([["🔙 بازگشت"]], resize_keyboard=True)
            await message.reply(LAST_NUMBER_ERROR_TEXT, reply_markup=keyboard)
            return

        elif 5000000 >= int(message.text) >= 10000:
            list_inline = []
            # check ghoghnoos pay status
            if cohandler.config["settings"]["ghoghnoos_payment"] == "True":
                list_inline.append([InlineKeyboardButton("💳 پرداخت با کارت به کارته خودکار",f"paywithcard:{message.text}")])
            
            # check crypto payment status
            if cohandler.config["settings"]["crypto_payment"] == "True":
                list_inline.append([InlineKeyboardButton("💸 پرداخت با ارز دیجیتال",f"paywithnowpay:{message.text}")])
            
            # check crypto payment status
            if cohandler.config["settings"]["card_to_card_channel_payment"] == "True":
                list_inline.append([InlineKeyboardButton("💳 پرداخت ب صورت کارت به کارت",f"paywithc2c_custom:{message.text}")])

            keyboard = InlineKeyboardMarkup(list_inline)
            await message.reply(
                ADD_BALANCE_FINAL_TEXT.format(message.text), reply_markup=keyboard
            )

            return
        else:
            keyboard = ReplyKeyboardMarkup([["🔙 بازگشت"]], resize_keyboard=True)
            await message.reply(
                INVALID_ADD_BALANCE_VALUE_MESSAGE, reply_markup=keyboard
            )
            return


@app.on_callback_query(dynamic_data_filter("change_buy_status"))
async def change_buy_status(client, query):
    buystatus = (
        "✅ فعال" if cohandler.config["settings"]["buystatus"] == "True" else "❌ غیر فعال"
    )

    keybutton = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"🚦 وضعیت : {buystatus}", callback_data="good")],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"change_buy_statusOn"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"change_buy_statusOff"
                ),
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"backtoSettingmanage")],
        ]
    )

    await query.edit_message_text(CHANGE_BUY_STATUS, reply_markup=keybutton)


@app.on_callback_query(dynamic_data_filter("change_sponsor"))
async def change_sponsor(client, query):
    sponsor_channel = cohandler.config["bot"]["sponsor_channel"]

    keybutton = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✏️ تغییر کانال", callback_data=f"send_channel")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"backtoSettingmanage")],
        ]
    )

    await query.edit_message_text(
        "کانال فعلی : {} ".format(sponsor_channel), reply_markup=keybutton
    )


@app.on_callback_query(dynamic_data_filter("send_channel"))
async def change_sponsor(client, query):
    await app.send_message(
        query.from_user.id, SEND_SPONSOR_CHANEL, reply_markup=ADD_BALANCE_CANCEL_BUTTON
    )
    await db.updateUserStep(query.from_user.id, "send_channel")


@app.on_callback_query(dynamic_data_filter("change_buy_statusOn"))
async def change_buy_statusOn(client, query):
    cohandler.update_config("bot", "buystatus", "True")
    buystatus = (
        "✅ فعال" if cohandler.config["settings"]["buystatus"] == "True" else "❌ غیر فعال"
    )

    keybutton = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"🚦 وضعیت : {buystatus}", callback_data="good")],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"change_buy_statusOn"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"change_buy_statusOff"
                ),
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"backtoSettingmanage")],
        ]
    )

    try:
        await query.edit_message_reply_markup(reply_markup=keybutton)
    except Exception as ex:
        logger(__name__).error(ex)


@app.on_callback_query(dynamic_data_filter("change_buy_statusOff"))
async def change_buy_statusOff(client, query):
    cohandler.update_config("bot", "buystatus", "False")
    buystatus = (
        "✅ فعال" if cohandler.config["settings"]["buystatus"] == "True" else "❌ غیر فعال"
    )

    keybutton = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"🚦 وضعیت : {buystatus}", callback_data=f"good")],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"change_buy_statusOn"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"change_buy_statusOff"
                ),
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"backtoSettingmanage")],
        ]
    )

    try:
        await query.edit_message_reply_markup(reply_markup=keybutton)
    except Exception as ex:
        logger(__name__).error(ex)


@app.on_callback_query(dynamic_data_filter("BackToServers"))
async def Choseserver(client, query):
    servers = await unknownApi.GetServers()
    server_list = [server for server in servers["servers"] if server["enabled"] == True]

    buttons = []

    for row in list(chunks(server_list, 3)):
        row_list = []
        for server in row:
            row_list.append(
                InlineKeyboardButton(
                    text=server["name"], callback_data=f"Buyservice:{server['id']}"
                )
            )
        buttons.append(row_list)

    buttons.append([InlineKeyboardButton("❌بستن پنل❌", callback_data=f"close")])

    await query.edit_message_text(
        SERVERS_TEXT, reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(dynamic_data_filter("Buyservice"))
async def BuyServiceTime(client, query):
    server_id = query.data.split(":")[1]
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("یکماهه", f"BuyServiceTime:{server_id}:{1}")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"BackToServers")],
        ]
    )
    await query.edit_message_text(TIME_SERVICE_TEXT, reply_markup=keyboard)


@app.on_callback_query(dynamic_data_filter("BuyServiceTime"))
async def BuyServiceUser(client, query):
    server_id = query.data.split(":")[1]
    CHtime = int(query.data.split(":")[2])
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "یک کاربره", f"BuyServiceUser:{server_id}:{CHtime}:{1}"
                ),
                InlineKeyboardButton(
                    "دو کاربره", f"BuyServiceUser:{server_id}:{CHtime}:{2}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "سه کاربره", f"BuyServiceUser:{server_id}:{CHtime}:{3}"
                ),
                InlineKeyboardButton(
                    "چهار کاربره", f"BuyServiceUser:{server_id}:{CHtime}:{4}"
                ),
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"Buyservice:{server_id}")],
        ]
    )
    await query.edit_message_text(USERS_COUNT_TEXT, reply_markup=keyboard)


@app.on_callback_query(dynamic_data_filter("BuyServiceUser"))
async def BuyServiceSize(client, query):
    server_id = query.data.split(":")[1]
    CHtime = int(query.data.split(":")[2])
    user_count = int(query.data.split(":")[3])
    keyboard = []

    keyboard = [
        [
            InlineKeyboardButton(
                f"{i} گیگ", f"buyfinal:{server_id}:{CHtime}:{user_count}:{i}"
            )
        ]
        for i in prices.size[user_count]
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 بازگشت", callback_data=f"BuyServiceTime:{server_id}:{CHtime}"
            )
        ]
    )

    await query.edit_message_text(
        SIZES_TEXT, reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(dynamic_data_filter("buyfinal"))
async def BuyServiceSize(client, query):
    UserId = query.from_user.id
    server_id = query.data.split(":")[1]
    CHtime = int(query.data.split(":")[2])
    user_count = int(query.data.split(":")[3])
    size = int(query.data.split(":")[4])
    price = prices.size[int(user_count)][int(size)]
    timed = "یکماهه"
    keyboard = []
    payment_id = await db.insertPayments(
        UserId, price, detail=f"BuyService_{server_id}_{user_count}_{size}_{CHtime}"
    )

    servers = await unknownApi.GetServers()
    for i in servers["servers"]:
        if i["id"] == server_id:
            loaction = i["name"]

    keyboard = InlineKeyboardMarkup(
        [
            # [InlineKeyboardButton('🏦 پرداخت با  درگاه بانکی ',f'Buypayrial:{payment_id.inserted_id}')],
            [
                InlineKeyboardButton(
                    "💰 پرداخت  از کیف پول", f"paywithbalance:{payment_id.inserted_id}"
                )
            ],
            # [InlineKeyboardButton('💸 پرداخت با ارز دیجیتال',f'buypaywithnow:{payment_id.inserted_id}')],
            [
                InlineKeyboardButton(
                    "💳 پرداخت ب صورت کارت به کارت",
                    f"buypaywithcard:{payment_id.inserted_id}",
                )
            ],
        ]
    )
    await query.edit_message_text(
        FINAL_STAGE_TEXT.format(
            payment_id.inserted_id, loaction, timed, user_count, size, price
        ),
        reply_markup=keyboard,
    )


@app.on_callback_query(dynamic_data_filter("getConnections"))
async def GetServiceConn(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer("سرویس پیدا نشد")
        return
    conn = await unknownApi.GetServiceConn(license)
    if conn and conn["status"] == True:
        await query.edit_message_text(
            SERVICE_CONNECTIONS_TEXT.format(
                serviceinfo["service"]["name"], "\n".join(conn["connections"])
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                        )
                    ]
                ]
            ),
        )
        return
    else:
        await apiQueryErrorHandler(conn, query)


@app.on_callback_query(dynamic_data_filter("addsizeto"))
async def addsizeto(client, query):
    license = query.data.split(":")[1]
    size = int(query.data.split(":")[2])
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    user = await db.get_user(query.from_user.id)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer("سرویس پیدا نشد")
        return
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("✅ تایید", f"moresize:{license}:{size}:Confirm")],
                [InlineKeyboardButton("🔙 بازگشت", f"moresize:{license}:{size}:back")],
            ]
        )
        await query.edit_message_text(
            FINAL_ADD_SIZE_TEXT.format(
                serviceinfo["service"]["name"],
                size,
                user["balance"],
                prices.data * size,
            ),
            reply_markup=keyboard,
        )


@app.on_callback_query(dynamic_data_filter("moresize"))
async def addsizeto(client, query):
    UserId = query.from_user.id
    license = query.data.split(":")[1]
    size = int(query.data.split(":")[2])
    price = prices.data * size
    user = await db.get_user(query.from_user.id)
    userbalance = user["balance"]
    if query.data.split(":")[-1] == "back":
        await db.updateUserStep(UserId, f"addsize:{license}")
        keyboard = ReplyKeyboardMarkup([["🔙 بازگشت"]], resize_keyboard=True)
        await query.edit_message_text(INCREASE_SIZE_TEXT, reply_markup=keyboard)
        return
    if int(price) > userbalance:
        await query.answer(LESS_BALANCE_TEXT)
        return
    else:
        service = await unknownApi.getApiServiceInfo(license)
        if service == None or service["status"] == False:
            await app.send_message(UserId, ADD_SIZE_ERROR, reply_markup=HELLO_BUTTONS)
            await db.updateUserStep(UserId, "Home")
            return
        status = await db.MakeBuyTransection(UserId, int(price))
        if status:
            BuyStatus = await unknownApi.buyMoreTraffic(
                service["service"]["id"], int(size)
            )
            if BuyStatus and BuyStatus["status"]:
                await db.insertPayments(
                    UserId,
                    int(size) * prices.size,
                    "Done",
                    f"BuyMore_Size_{service['service']['id']}_{size}",
                )
                await query.edit_message_text(SUCCESSFULL_ADD_SIZE_USER_TEXT)
                await app.send_message(
                    UserId, CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS
                )
                await db.updateUserStep(UserId, "Home")
                return
            else:
                if BuyStatus:
                    if BuyStatus["message"] == "too low expiry time":
                        await query.edit_message_text(CANT_ADD_SIZE_ERROR)
                        await app.send_message(
                            UserId, CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS
                        )
                    else:
                        await apiQueryErrorHandler(BuyStatus, query)
                else:
                    await apiQueryErrorHandler(BuyStatus, query)
                await db.inc_user_amount(UserId, int(price))
                await db.updateUserStep(UserId, "Home")
                return
        else:
            await query.edit_message_text(LESS_BALANCE_TEXT)
            await app.send_message(
                UserId, CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS
            )
            await db.updateUserStep(UserId, "Home")


@app.on_callback_query(
    dynamic_data_filter("getservice") | dynamic_data_filter("backtoServicemanage")
)
async def getservice(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer("سرویس پیدا نشد")
        return
    ServiceManageButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔗دریافت لینک نیم بها", callback_data=f"getnimbahalink:{license}"
                )
            ],
            [
                InlineKeyboardButton(
                    "📝 تغییر نام سرویس", callback_data=f"changeServiceName:{license}"
                ),
                InlineKeyboardButton(
                    "📊 مشخصات سرویس", callback_data=f"getinfo:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ کاربر اضافه", callback_data=f"adduser:{license}"
                ),
                InlineKeyboardButton(
                    "⚡️ تغییر لینک اتصال", callback_data=f"changeLinks:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "♾ تمدید خودکار", callback_data=f"autopay:{license}"
                ),
                InlineKeyboardButton(
                    "🔄 تغییر لوکیشن", callback_data=f"chgLocation:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "📣 هشدار های اتصال", callback_data=f"coAlarm:{license}"
                ),
                InlineKeyboardButton(
                    "🧬 افراد متصل", callback_data=f"getConnections:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔥 تغییر پروتکل", callback_data=f"changeprotocol:{license}"
                )
            ],
            [InlineKeyboardButton("🔙 بازگشت", callback_data=f"backtoServiceList")],
        ]
    )

    name = (
        serviceinfo["service"]["server_name"].split(" ")[0]
        + " "
        + serviceinfo["service"]["name"]
    )
    location = serviceinfo["service"]["server_name"]
    protocol = serviceinfo["service"]["protocol"]
    _type = serviceinfo["service"]["type"]
    status = "فعال" if serviceinfo["service"]["enabled"] == True else "غیر فعال"
    Id = serviceinfo["service"]["id"]
    msgtxt = SERVICE_INFO_TEXT2.format(
        name, location, protocol, _type, status, Id, license
    )
    await query.edit_message_text(msgtxt, reply_markup=ServiceManageButton)
    return


@app.on_callback_query(dynamic_data_filter("changeprotocol"))
async def ChangeProtocol(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    vmess = "✅ Vmess" if serviceinfo["service"]["protocol"] == "vmess" else "Vmess"
    vless = "✅ Vless" if serviceinfo["service"]["protocol"] == "vless" else "Vless"

    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(vmess, callback_data=f"changeto:{license}:vmess"),
                InlineKeyboardButton(vless, callback_data=f"changeto:{license}:vless"),
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )
    await query.edit_message_text(CHANGE_PROTOCOL_TEXT, reply_markup=keybutton)
    return


@app.on_callback_query(dynamic_data_filter("changeLinks"))
async def ChangeLinks(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    logger(__name__).info(serviceinfo)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ تایید", callback_data=f"ChangelinkConfirmed:{license}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )
    await query.edit_message_text(CONFIRM_CHANGE_LINK_TEXT, reply_markup=keybutton)
    return


@app.on_callback_query(dynamic_data_filter("chgLocation"))
async def ChangeLocation(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return

    servers = await unknownApi.GetServers()
    server_list = choices(
        [server for server in servers["servers"] if server["enabled"] == True], k=30
    )

    buttons = []

    for row in list(chunks(server_list, 3)):
        row_list = []
        for server in row:
            row_list.append(
                InlineKeyboardButton(
                    text=server["name"], callback_data=f"Cgto:{license}:{server['id']}"
                )
            )
        buttons.append(row_list)

    buttons.append([InlineKeyboardButton("❌بستن پنل❌", callback_data=f"close")])

    await query.edit_message_text(
        CHANGE_LOCATION_TEXT, reply_markup=InlineKeyboardMarkup(buttons)
    )
    return


@app.on_callback_query(dynamic_data_filter("add_balance"))
async def add_balance(client, query):
    keyboard = ReplyKeyboardMarkup([["🔙 بازگشت"]], resize_keyboard=True)
    await query.edit_message_text(ADD_BALANCE_TEXT, reply_markup=keyboard)
    await db.updateUserStep(query.from_user.id, "addbalance")


@app.on_callback_query(dynamic_data_filter("Cgto"))
async def ChangServerto(client, query):
    license = query.data.split(":")[1]
    server_id = query.data.split(":")[2]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    elif serviceinfo["service"]["server_id"] == query.data.split(":")[2]:
        await query.answer(ALREADY_THIS_LOCATION_TEXT)
        return
    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ تایید", callback_data=f"Cgtoconf:{license}:{server_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )
    await query.edit_message_text(CONFIRM_CHANGE_LOCATION_TEXT, reply_markup=keybutton)
    return


@app.on_callback_query(dynamic_data_filter("ChangelinkConfirmed"))
async def CoChangeLinks(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    status = await unknownApi.ChangeLink(license)
    if status and status["status"] == True:
        service = await unknownApi.getservicelinks(license) # Bug
        await db.updateServicelink(license, service["direct"])
        keybutton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔗 دریافت لینک نیم بها",
                        callback_data=f"getnimbahalink:{license}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت", callback_data=f"changeLocation:{license}"
                    )
                ],
            ]
        )
        await query.edit_message_text(
            CHANGED_LINK_SUCCESSFULLY_TEXT, reply_markup=keybutton
        )
        await db.updateUserStep(query.from_user.id, "Home")
        return
    else:
        await apiQueryErrorHandler(status, query, "link")


@app.on_callback_query(dynamic_data_filter("Cgtoconf"))
async def CoChangeLocation(client, query):
    license = query.data.split(":")[1]
    server_id = query.data.split(":")[2]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    status = await unknownApi.ChangeLocation(license, server_id)
    if status and status["status"] == True:
        keybutton = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔗 دریافت لینک نیم بها",
                        callback_data=f"getnimbahalink:{license}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت", callback_data=f"changeLinks:{license}"
                    )
                ],
            ]
        )
        await query.edit_message_text(
            LOCATION_CHANGED_SUCCESSFULLY_TEXT, reply_markup=keybutton
        )
        await db.updateUserStep(query.from_user.id, "Home")
        return
    else:
        await apiQueryErrorHandler(status, query, "location")


@app.on_callback_query(dynamic_data_filter("autopay"))
async def ChangeAutoPay(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    if len(query.data.split(":")) == 3:
        if query.data.split(":")[2] == "off":
            await db.SetVpnServiceAutopay(license, False)
        elif query.data.split(":")[2] == "on":
            await db.SetVpnServiceAutopay(license, True)
        elif query.data.split(":")[2] == "status":
            await query.answer(":|")
            return

    service = await db.getServiceInfo(license)
    autopaystatus = "✅ فعال" if service["autopay"] == True else "❌ غیر فعال"

    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"🚦 وضعیت : {autopaystatus}",
                    callback_data=f"autopay:{license}:status",
                )
            ],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"autopay:{license}:on"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"autopay:{license}:off"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )
    try:
        await query.edit_message_reply_markup(reply_markup=keybutton)
    except:
        pass


@app.on_callback_query(dynamic_data_filter("CoAlarmoff"))
async def ChangeAlarmoff(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    await db.SetVpnServiceAlarm(license, False)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    service = await db.getServiceInfo(license)
    autopaystatus = "✅ فعال" if service["alarm"] == True else "❌ غیر فعال"

    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"🚦 وضعیت : {autopaystatus}",
                    callback_data=f"coAlarm:{license}:status",
                )
            ],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"CoAlarmon:{license}"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"CoAlarmoff:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )

    try:
        await query.edit_message_reply_markup(reply_markup=keybutton)
    except:
        pass


@app.on_callback_query(dynamic_data_filter("CoAlarmon"))
async def ChangeAlarmon(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    await db.SetVpnServiceAlarm(license, True)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    service = await db.getServiceInfo(license)
    autopaystatus = "✅ فعال" if service["alarm"] == True else "❌ غیر فعال"

    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"🚦 وضعیت :{autopaystatus}",
                    callback_data=f"coAlarm:{license}:status",
                )
            ],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"CoAlarmon:{license}"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"CoAlarmoff:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )
    try:
        await query.edit_message_reply_markup(reply_markup=keybutton)
    except:
        pass


@app.on_callback_query(dynamic_data_filter("coAlarm"))
async def ChangeAlarm(client, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return
    service = await db.getServiceInfo(license)
    autopaystatus = "✅ فعال" if service["alarm"] == True else "❌ غیر فعال"

    keybutton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"🚦 وضعیت : {autopaystatus}",
                    callback_data=f"coAlarm:{license}:status",
                )
            ],
            [
                InlineKeyboardButton("✅ فعال", callback_data=f"CoAlarmon:{license}"),
                InlineKeyboardButton(
                    "❌ غیر فعال", callback_data=f"CoAlarmoff:{license}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                )
            ],
        ]
    )

    await query.edit_message_text(SHOW_ALERTS_TEXT, reply_markup=keybutton)


@app.on_callback_query(dynamic_data_filter("changeServiceName"))
async def ChangeServiceName(self, query):
    license = query.data.split(":")[1]

    await app.delete_messages(query.from_user.id, query.message.id)
    await app.send_message(
        query.from_user.id,
        text=CHANGE_SERVICE_NAME_TEXT,
        reply_markup=CHANGE_SERVICE_BACK,
    )
    await db.updateUserStep(query.from_user.id, f"changename:{license}")


@app.on_callback_query(dynamic_data_filter("getinfo"))
async def GetServiceInfo(self, query):
    license = query.data.split(":")[1]
    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if serviceinfo == None or serviceinfo["status"] == False:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return

    if serviceinfo["status"] == False:
        await apiQueryErrorHandler(serviceinfo, query)
        return
    else:
        expiryTime = serviceinfo["service"]["expiryTime"]
        utcExpire = date.utcfromtimestamp(expiryTime)
        jalali_Expire = jdate.fromgregorian(datetime=utcExpire)
        now = jdate.now()
        daysleft = jalali_Expire - now
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔙 بازگشت", callback_data=f"backtoServicemanage:{license}"
                    )
                ]
            ]
        )
        txt = GET_SERVICE_INFO_TEXT.format(
            f"{serviceinfo['service']['server_name'].split(' ')[0]} {serviceinfo['service']['name']}",
            serviceinfo["service"]["server_name"],
            "فعال ✅" if serviceinfo["service"]["enabled"] else "غیر فعال ❌",
            serviceinfo["service"]["protocol"],
            serviceinfo["service"]["type"],
            daysleft.days,
            serviceinfo["service"]["users_count"],
            serviceinfo["service"]["size"],
            serviceinfo["service"]["used_size"],
            serviceinfo["service"]["remain_size"],
            serviceinfo["service"]["plan"],
            prices.service_dict[serviceinfo["service"]["price"]],
            serviceinfo["service"]["createdTime"].split(" ")[0],
            serviceinfo["service"]["createdTime"].split(" ")[1],
        )
        await query.edit_message_text(txt, reply_markup=keyboard)
        return


@app.on_callback_query(dynamic_data_filter("getnimbahalink"))
async def SendQR(self, query):
    license = query.data.split(":")[1]

    serviceinfo = await unknownApi.getApiServiceInfo(license)
    if not serviceinfo:
        await query.answer(SERVICE_NOT_FOUND_TEXT)
        return

    if not serviceinfo["status"]:
        await apiQueryErrorHandler(serviceinfo, query, "link")
        return

    dir_link = await unknownApi.getservicelinks(license)
    if not dir_link:
        return await apiQueryErrorHandler({"message": "unknown"}, query)

    if dir_link["status"]:
        data = change_config_name(
            dir_link["direct"],
            serviceinfo["service"]["name"],
            serviceinfo["service"]["server_name"].split(" ")[0],
        )
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        byte_io = io.BytesIO()
        img.save(byte_io, "PNG")
        byte_io.seek(0)
        await app.send_photo(
            query.from_user.id, photo=byte_io, caption=QRCODE_STRING.format(data)
        )

    else:
        await apiQueryErrorHandler(dir_link, query, "link")


@app.on_callback_query(dynamic_data_filter("changeto"))
async def ChangeProtocolto(client, query):
    license = query.data.split(":")[1]
    protocol = query.data.split(":")[2]
    status = await unknownApi.ChangeServiceProtocol(license, protocol)

    if status:
        if status["status"] == False:
            await apiQueryErrorHandler(status, query, "protocol")
            return
        else:
            serviceinfo = await unknownApi.getApiServiceInfo(license)
            if not serviceinfo:
                await query.answer(SERVICE_NOT_FOUND_TEXT)
                return

            if not serviceinfo["status"]:
                return await apiQueryErrorHandler(dir_link, query, "link")

            dir_link = await unknownApi.getservicelinks(license)
            await db.updateServicelink(
                license,
                dir_link["direct"],
                serviceinfo["service"]["name"],
                serviceinfo["service"]["server_name"].split(" ")[0],
            )

            keybutton = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔗 دریافت لینک نیم بها",
                            callback_data=f"getnimbahalink:{license}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔙 بازگشت", callback_data=f"changeprotocol:{license}"
                        )
                    ],
                ]
            )
            await query.edit_message_text(
                CHANGE_PROTOCOL_SUCCESSFULL_TEXT, reply_markup=keybutton
            )
            return
    else:
        await query.answer(UNKNOWN_ERROR)
        return


@app.on_callback_query(dynamic_data_filter("backtoServiceList"))
async def BackToServiceList(client, query):
    user_services_list = await db.get_user_services(query.from_user.id)
    servicebuttons = []
    if user_services_list:
        for services in user_services_list:
            ser = await unknownApi.getApiServiceInfo(services["license"])
            if ser:
                servicebuttons.append(
                    [
                        InlineKeyboardButton(
                            f"{services['flag']} {services['name']}",
                            callback_data=f"getservice:{services['license']}",
                        )
                    ]
                )
        servicebuttons.append(
            [InlineKeyboardButton("❌بستن پنل❌", callback_data=f"close")]
        )
        await query.edit_message_text(
            MANAGE_SERVICES_TEXT, reply_markup=InlineKeyboardMarkup(servicebuttons)
        )
    else:
        await query.edit_message_text(NO_SERVICES_TEXT)

    return


@app.on_callback_query(dynamic_data_filter("paywithnow"))
async def Paywithnow(client, query):
    amount = int(query.data.split(":")[-1])
    keyboard = [
        [InlineKeyboardButton(f"⭐️{SOFT_COINS_NAME[i]}⭐️", f"pay:{i}:{amount}")]
        for i in SOFT_COINS_NAME
    ]
    await query.edit_message_text(
        CHOICE_COIN_TEXT, reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return


@app.on_callback_query(dynamic_data_filter("paywithrial"))
async def Paywithrial(client, query):
    UserId = query.from_user.id
    amount = float(query.data.split(":")[-1])

    # if amount < float(cohandler.config["bot"]["rialMinLimit"]):
    #     await query.answer(
    #         RIAL_MIN_LIMIT_TEXT.format(cohandler.config["bot"]["rialMinLimit"])
    #     )
    #     return
    # elif amount > float(cohandler.config["bot"]["rialMaxLimit"]):
    #     await query.answer(
    #         RIAL_MAX_LIMIT_TEXT.format(cohandler.config["bot"]["rialMaxLimit"])
    #     )
    #     return

    # dollar = await nowapi.GetDollarPrice()
    # status = await nowapi.CreatePayment(
    #     "trx", amount / dollar, f"ADD_BALANCE_{amount/dollar}_dollar_{UserId}"
    # )
    # try:
    #     payurl = ""
    #     keyboard = [[InlineKeyboardButton("🏧 پرداخت 🏧", url=payurl)]]
    #     await query.edit_message_text(
    #         ADD_RIAL_TEXT.format(amount, status["payment_id"]),
    #         reply_markup=InlineKeyboardMarkup(keyboard),
    #     )
    #     await db.insertPayments(
    #         UserId,
    #         amount,
    #         detail=f"ADD_BALANCE_{amount/dollar}_dollar_{UserId}",
    #         payment_id=status["pay_address"],
    #     )

    #     return
    # except Exception as ex:
    #     logger(__name__).error(ex)


@app.on_callback_query(dynamic_data_filter("Buypayrial"))
async def Paywithrial(client, query):
    UserId = query.from_user.id
    if cohandler.config["settings"]["buystatus"] != "True":
        await query.answer(CANT_BUY_TEXT)
        return

    # payment_id = query.data.split(":")[1]
    # payment = await db.get_payment(payment_id)
    # _, server_id, user_count, size, CHtime = payment["detail"].split("_")

    # amount = float(prices.size[int(user_count)][int(size)])
    # if amount < float(cohandler.config["bot"]["rialMinLimit"]):
    #     await query.answer(RIAL_MIN_LIMIT_TEXT)
    #     return
    # elif amount > float(cohandler.config["bot"]["rialMaxLimit"]):
    #     await query.answer(RIAL_MAX_LIMIT_TEXT)

    # dollar = await nowapi.GetDollarPrice()
    # status = await nowapi.CreatePayment(
    #     "trx", amount / dollar, f"BuyService_{server_id}_{user_count}_{size}_{CHtime}"
    # )
    # try:
    #     await db.updatePayment_Id(payment["_id"], status["payment_id"])
    #     payurl = ""
    #     keyboard = [[InlineKeyboardButton("🏧 پرداخت 🏧", url=payurl)]]
    #     await query.edit_message_text(
    #         RIAL_PAY_TEXT.format(payment["_id"], CHtime, user_count, size, amount),
    #         reply_markup=InlineKeyboardMarkup(keyboard),
    #     )
    #     return
    # except Exception as ex:
    #     logger(__name__).error(ex)
    #     await query.answer(RIALERROR_TEXT)


@app.on_callback_query(dynamic_data_filter("paywithcard"))
async def Paywithnow(client, query):
    UserId = query.from_user.id

    amount = int(query.data.split(":")[-1])
    detail = f"ADD_BALANCE_{amount}_rial_{UserId}"
    order_id = await db.insertPayments(UserId, amount, "pending", detail)
    await db.updateUserStep(UserId, f"Enter_card:{order_id.inserted_id}")
    await query.edit_message_text(ENTER_CARD_TEXT, reply_markup=PAY_CARD_BUTTONS)


@app.on_callback_query(dynamic_data_filter("buypaywithcard"))
async def buypaywithcard(client, query):
    UserId = query.from_user.id
    if cohandler.config["settings"]["buystatus"] != "True":
        await query.answer(CANT_BUY_TEXT)
        return
    payment_id = query.data.split(":")[1]
    await db.updateUserStep(UserId, f"Enter_card:{payment_id}")
    await query.edit_message_text(ENTER_CARD_TEXT, reply_markup=PAY_CARD_BUTTONS)
    return


@app.on_callback_query(dynamic_data_filter("buypaywithnow"))
async def BuyPaywithnow(client, query):
    UserId = query.from_user.id
    if cohandler.config["settings"]["buystatus"] != "True":
        await query.answer(CANT_BUY_TEXT)
        return
    payment_id = query.data.split(":")[1]
    keyboard = [
        [InlineKeyboardButton(f"⭐️{SOFT_COINS_NAME[i]}⭐️", f"pay:{i}:{payment_id}")]
        for i in SOFT_COINS_NAME
    ]
    await query.edit_message_text(
        CHOICE_COIN_TEXT, reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return


@app.on_callback_query(dynamic_data_filter("paywithbalance"))
async def paywithbalance(client, query):
    status = await unknownApi.GetAccInfo()
    if not status:
        return await query.reply(UNKNOWN_ERROR)

    if not status["status"]:
        logger(__name__).info(status)
        return await apiMsgErrorHandler(status, query)

    if status["balance"] < 500_000:
        await app.send_message(
            cohandler.config["bot"]["admin"],
            "❌ موجودی حساب کمتر از 500 هزار تومن است.\nلطفا موجودی Unknown را شارژ کنید.",
        )
        return await query.reply(
            "⚠️ بخش فروش فعلا در دسترس نمیباشد.\nلطفا با پشتیبانی در ارتباط باشید.\n\n🆔 @"+cohandler.config["bot"]["sponsor_admin"]
        )

    UserId = query.from_user.id
    if cohandler.config["settings"]["buystatus"] != "True":
        await query.answer(CANT_BUY_TEXT)
        return
    payment_id = query.data.split(":")[1]
    payment = await db.get_payment(payment_id)
    _, server_id, user_count, size, CHtime = payment["detail"].split("_")
    amount = prices.size[int(user_count)][int(size)]
    user = await db.get_user(UserId)
    userbalance = user["balance"]
    if int(amount) > userbalance:
        await query.answer(LESS_BALANCE_TEXT)
        return
    else:
        status = await db.MakeBuyTransection(UserId, int(amount))
        if status:
            BuyStatus = await unknownApi.createService(
                server_id, int(CHtime), int(size), int(user_count)
            )
            if BuyStatus and BuyStatus["status"]:
                ServiceInfo = await unknownApi.getApiServiceInfo(BuyStatus["license"])
                dir_link = await unknownApi.getservicelinks(BuyStatus["license"])
                await db.insertNewVpnService(
                    ServiceInfo["service"]["name"],
                    UserId,
                    BuyStatus["license"],
                    ServiceInfo["service"]["server_name"].split(" ")[0],
                    int(size),
                    int(user_count),
                    dir_link=dir_link["direct"],
                )

                await query.edit_message_text(
                    SUCCESSFULL_BUY.format(payment_id, CHtime, user_count, size)
                )
                await db.insertPayments(
                    UserId,
                    int(amount),
                    "Done",
                    f"BuyService_WithPalance_{BuyStatus['license']}",
                )
                await admin_logger.new_service_log(
                    app,
                    "Balance",
                    UserId,
                    payment_id,
                    BuyStatus['license'],
                    ServiceInfo["service"]["name"],
                    CHtime,
                    user_count,
                    size,
                    f"{int(amount):,}"
                    )
                
                user = await db.get_user(UserId)
                if user["refferal"]:
                    await db.inc_user_amount(user["refferal"], prices.giftAmount)
                    await app.send_message(
                        user["refferal"], REF_BUY_SUCESSS.format(prices.giftAmount)
                    )
                return
            else:
                if BuyStatus:
                    if BuyStatus["message"] == "server full":
                        await query.edit_message_text(
                            BALANCE_EXCEPT_BUY2.format(payment_id)
                        )
                    elif BuyStatus["message"] == "buy disabled":
                        await query.edit_message_text(
                            BALANCE_EXCEPT_BUY2.format(payment_id)
                        )
                    else:
                        await apiQueryErrorHandler(BuyStatus, query)
                else:
                    await apiQueryErrorHandler(BuyStatus, query)
                await db.inc_user_amount(UserId, int(amount))

                return
        else:
            await query.answer(LESS_BALANCE_TEXT)


@app.on_callback_query(dynamic_data_filter("pay"))
async def PayCoin(client, query):
    status = await unknownApi.GetAccInfo()
    if not status:
        return await query.reply(UNKNOWN_ERROR)

    if not status["status"]:
        logger(__name__).info(status)
        return await apiMsgErrorHandler(status, query)

    if status["balance"] < 500_000:
        await app.send_message(
            cohandler.config["bot"]["admin"],
            "❌ موجودی حساب کمتر از 500 هزار تومن است.\nلطفا موجودی Unknown را شارژ کنید.",
        )
        return await query.reply(
            "⚠️ بخش فروش فعلا در دسترس نمیباشد.\nلطفا با پشتیبانی در ارتباط باشید.\n\n🆔 @"+cohandler.config["bot"]["sponsor_admin"]
        )

    UserId = query.from_user.id
    coin = query.data.split(":")[1]
    if cohandler.config["settings"]["buystatus"] != "True":
        await query.answer(CANT_BUY_TEXT)
        return
    payment_id = query.data.split(":")[2]
    payment = await db.get_payment(payment_id)
    price = await nowapi.GetDollarPrice()
    if not price:
        await query.answer("خطایی رخ داده است بعدا دوباره تلاش کنید")
        return
    if "ADD_BALANCE_" in payment["detail"]:
        amount = payment["amount"]
        status = await nowapi.CreatePayment(
            coin, amount / price, f"ADD_BALANCE_{amount/price}_dollar_{UserId}"
        )
    else:
        amount = payment["amount"]
        status = await nowapi.CreatePayment(
            coin, amount / price, f"BuyService_{amount/price}_dollar_{UserId}"
        )

    if status:
        target_time = date.strptime(status["valid_until"], "%Y-%m-%dT%H:%M:%S.%fZ")
        current_time = date.utcnow()
        if "payin_extra_id" in status:
            memo = status["payin_extra_id"]
        else:
            memo = "_"
        remaining_time = target_time - current_time
        remaining_days = remaining_time.days
        remaining_hours, remainder_minutes = divmod(remaining_time.seconds, 3600)
        remaining_minutes, _ = divmod(remainder_minutes, 60)

        expirin = f"مهلت پرداخت: {remaining_days}روز و {remaining_hours}ساعت و {remaining_minutes}دقیقه"
        await db.updatePayment_Id(payment_id, payment_id=status["payment_id"])
        msg_txt = CRYPTO_PAY_TEXT.format(
            payment_id,
            status["payment_id"],
            status["order_description"],
            amount / price,
            status["pay_amount"],
            status["pay_currency"],
            status["network"],
            status["pay_address"],
            memo,
            expirin,
        )

        data = status["pay_address"]
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        byte_io = io.BytesIO()
        img.save(byte_io, "PNG")

        # Reset the file position to the beginning
        byte_io.seek(0)
        await app.send_photo(
            query.from_user.id,
            photo=byte_io,
            caption=msg_txt,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔍 بررسی وضعیت پرداخت", f"check:{payment_id}")]]
            ),
        )

        await app.send_message(
            UserId, CANCEL_ADD_BALANCE_TEXT, reply_markup=HELLO_BUTTONS
        )
        await db.updateUserStep(UserId, "Home")
    else:
        await query.answer(UNKNOWN_ERROR)
        await app.send_message(
            cohandler.config["bot"]["admin"],
            ERROR_TEXT.format(status["statusCode"], status["code"], status["message"]),
        )


@app.on_callback_query(dynamic_data_filter("check"))
async def checkpayment(client, query):
    UserId = query.from_user.id
    payment_id = query.data.split(":")[1]
    payment = await db.get_payment(payment_id)
    status = await nowapi.PaymentStatus(payment["payment_id"])
    if status:
        if status["payment_status"] == "finished":
            payment = await db.get_payment(payment_id)
            # check payment have  pending status
            if payment and payment["status"] == "pending":
                await db.updatePaymentStatus(payment_id, "Done")
                if "BuyService" in payment["detail"]:
                    _, server_id, user_count, size, CHtime = payment["detail"].split(
                        "_"
                    )
                    await CreateService(
                        server_id, int(CHtime), int(size), int(user_count), app, payment
                    )
                    return
                elif "ADD_BALANCE" in payment["detail"]:
                    await query.edit_message_text(
                        SUCCESSFULL_ADD_BALANCE.format(payment_id)
                    )
                    await db.inc_user_amount(UserId, payment_id["amount"])
        elif status["payment_status"] == "refunded":
            await query.edit_message_text(TRANSACTION_REFUNDED_TEXT.format(payment_id))
            await db.updatePaymentStatus(payment_id, "refunded")
        elif status["payment_status"] == "waiting":
            await query.answer(TRANSACTION_WATING, show_alert=True)
        elif status["payment_status"] == "partially_paid":
            await query.edit_message_text(TRANSACTION_PARTIALLY_PAID.format(payment_id))
        elif status["payment_status"] == "failed":
            await query.edit_message_text(TRANSACTION_FAILED_TEXT.format(payment_id))
        elif status["payment_status"] == "expired":
            await query.edit_message_text(EXPIRED_MESSAGE_CRYPTO.format(payment_id))
        elif status["payment_status"] == "confirmed":
            await query.edit_message_text(TRANSACTION_RECEIVED_TEXT.format(payment_id))
    else:
        await query.answer(GATEWAY_ERROR_TEXT)
    return


@app.on_callback_query(dynamic_data_filter("close"))
async def closePanel(client, query):
    try:
        await query.message.delete()
    except Exception as ex:
        logger(__name__).error(ex)
        await query.edit_message_text(UNKNOWN_ERROR)
    return


@app.on_callback_query(
    dynamic_data_filter("how_connect") | dynamic_data_filter("back_how_connect")
)
async def how_connect_handler(client, query):
    await query.edit_message_text(HOWCONNECT_TEXT, reply_markup=HOWCONNECT_BUTTONS)
    return


@app.on_callback_query(dynamic_data_filter("androidcon"))
async def android_con_handler(client, query):
    await query.edit_message_text(
        ANDROID_TEXT, reply_markup=BUTTON_BACK_CONNECT, disable_web_page_preview=True
    )
    return


@app.on_callback_query(dynamic_data_filter("linuxcon"))
async def linux_con_handler(client, query):
    await query.edit_message_text(
        LINUX_TEXT, reply_markup=BUTTON_BACK_CONNECT, disable_web_page_preview=True
    )
    return


@app.on_callback_query(dynamic_data_filter("windowscon"))
async def win_con_handler(client, query):
    await query.edit_message_text(
        WINDOWS_TEXT, reply_markup=BUTTON_BACK_CONNECT, disable_web_page_preview=True
    )
    return


@app.on_callback_query(dynamic_data_filter("maccon"))
async def mak_con_handler(client, query):
    await query.edit_message_text(
        MAC_TEXT, reply_markup=BUTTON_BACK_CONNECT, disable_web_page_preview=True
    )
    return


@app.on_callback_query(dynamic_data_filter("ioscon"))
async def ios_con_handler(client, query):
    await query.edit_message_text(
        IOS_TEXT, reply_markup=BUTTON_BACK_CONNECT, disable_web_page_preview=True
    )
    return


@app.on_callback_query(dynamic_data_filter("adduser"))
async def Add_user(client, query):
    license = query.data.split(":")[1]
    current_info = await unknownApi.getApiServiceInfo(license)
    if current_info:
        await query.edit_message_text(MORE_USER_TEXT, reply_markup=CHANGE_SERVICE_BACK)
        await db.updateUserStep(query.from_user.id, f"adduser:{license}")
        # status = await unknownApi.AddUser(current_info['service']['id'])
    else:
        await apiQueryErrorHandler(current_info, query)


@app.on_message(filters.private & IsAdmin(app))
async def AdminStepHandler(client, message):
    UserId = message.from_user.id
    user = await db.get_user(UserId)
    if user == None:
        await db.insertNewUser(UserId, "Home", "admin")
        user = await db.get_user(UserId)
    userStep = user["step"]
    if userStep == "Send_PM":
        if message.text:
            if message.text == "🔙 بازگشت":
                await message.reply("منوی اصلی", reply_markup=ADMIN_MAIN_MENU)
                await db.updateUserStep(UserId, "Home")
                return
        keyboard = ReplyKeyboardMarkup(
            [["✅ تایید"], ["🔙 بازگشت"]], resize_keyboard=True
        )
        await db.updateUserStep(UserId, f"confirmPM:{message.chat.id}:{message.id}")
        await message.reply(CONFIRM_SEND_PM, reply_markup=keyboard)
        return
    elif userStep.split(":")[0] == "confirmPM":
        if message.text:
            if message.text == "🔙 بازگشت":
                await message.reply(SEND_PM_TEXT, reply_markup=keyboard)
                await db.updateUserStep(UserId, "Send_PM")
                return
            elif message.text == "✅ تایید":
                await db.updateUserStep(UserId, "Home")
                user_all = await db.get_all_users()
                PM_COUNT = 0
                ER_COUNT = 0
                await app.send_message(
                    UserId, "...درحال ارسال", reply_markup=ADMIN_MAIN_MENU
                )
                for i in user_all:
                    try:
                        await app.copy_message(
                            i["_id"],
                            int(userStep.split(":")[1]),
                            int(userStep.split(":")[2]),
                        )
                        PM_COUNT += 1
                        await asyncio.sleep(1)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except Exception as ex:
                        logger(__name__).error("sending message error :{%s}" % ex)
                        ER_COUNT += 1
                        continue
                await app.send_message(
                    UserId,
                    f" پیام ارسال  شد {PM_COUNT} ✅ \nتعداد خطا : {ER_COUNT} ❌",
                    reply_markup=ADMIN_MAIN_MENU,
                )
                return

    elif userStep == "send_channel":
        if message.text:
            if message.text == "🔙 بازگشت":
                await message.reply(
                    CANCEL_ADD_BALANCE_TEXT, reply_markup=ADMIN_MAIN_MENU
                )
                await db.updateUserStep(message.from_user.id, "Home")
                return
            else:
                cohandler.update_config("bot", "sponsor_channel", message.text)
                await message.reply("انجام شد", reply_markup=ADMIN_MAIN_MENU)
                await db.updateUserStep(message.from_user.id, "Home")
                return
            

async def apiMsgErrorHandler(status, query, type=None):
    if status:
        if status["message"] == "no change":
            await query.reply(PROTOCOL_IS_SAME)
            return
        elif status["message"] == "rate limited":
            if type == "protocol":
                await query.reply(CHANGE_PROTOCOL_FAST)
            elif type == "link":
                await query.reply(CHANGE_LINK_FAST_TEXT)
            elif type == "location":
                await query.reply(CHANGE_LOCATION_FAST_TEXT)
            elif type == "type":
                await query.reply(CHANGE_TYPE_FAST)
            elif type == "moreuser":
                await query.reply(MORE_USER_FAST)
            elif type == "name":
                await query.reply(CHNAGE_NAME_FAST)
            return
        elif status["message"] == "service expired":
            await query.reply(SERVICE_EXPIRED)
            return
        elif status["message"] == "service banned":
            await query.reply(SERVICE_BANNED_RAW_TEXT)
            return
        elif status["message"] == "invalid name":
            await query.reply(BAD_NAME_TEXT)
            return
        elif status["message"] == "same name":
            await query.reply(USED_NAME_TEXT)
            return
        elif status["message"] == "no balance":
            await query.reply(
                "پنل موجودی کافی برای انجام عملیات مورد نظر را نداد  لطفا به پشتیبانی اطلاع  دهید"
            )
            await app.send_message(cohandler.config["bot"]["admin"], "کمبود موجودی پنل")
        elif status["message"] == "maintenance":
            await query.reply(MAINTENANCE_SERVER_TEXT)
            return
        elif status["message"] == "unavailable":
            await query.reply(UNAVAILABLE_TEXT)
            return
        else:
            logger(__name__).error(status)
            await query.reply(UNKNOWN_ERROR)
            return
    await query.reply(UNKNOWN_ERROR)
    return


async def apiQueryErrorHandler(status, query, type=None):
    if status:
        if status["message"] == "no change":
            await query.answer(PROTOCOL_IS_SAME)
            return
        elif status["message"] == "rate limited":
            if type == "protocol":
                await query.answer(CHANGE_PROTOCOL_FAST)
            elif type == "link":
                await query.answer(CHANGE_LINK_FAST_TEXT)
            elif type == "location":
                await query.answer(CHANGE_LOCATION_FAST_TEXT)
            elif type == "type":
                await query.answer(CHANGE_TYPE_FAST)
            elif type == "name":
                await query.answer(CHNAGE_NAME_FAST)
        elif status["message"] == "service expired":
            await query.answer(SERVICE_EXPIRED)
        elif status["message"] == "service banned":
            await query.answer(SERVICE_BANNED_RAW_TEXT)
        elif status["message"] == "server full":
            await query.answer(SERVER_FULL_TEXT)
        elif status["message"] == "no balance":
            await query.answer(
                "پنل موجودی کافی برای انجام عملیات مورد نظر را نداد  لطفا به پشتیبانی اطلاع  دهید"
            )
            await app.send_message(cohandler.config["bot"]["admin"], "کمبود موجودی پنل")
        elif status["message"] == "same name":
            await query.answer(USED_NAME_TEXT)
            return
        elif status["message"] == "maintenance":
            await query.answer(MAINTENANCE_SERVER_TEXT)
            return
        elif status["message"] == "unavailable":
            await query.answer(UNAVAILABLE_TEXT)
            return
        else:
            logger(__name__).error(status)
            await query.answer(UNKNOWN_ERROR)
        return

    try:
        await query.answer(UNKNOWN_ERROR)
    except Exception as ex:
        logger(__name__).error(ex)
    return


async def main():
    logger(__name__).info("Running")
    await app.start()
    stopev = asyncio.Event()
    notifier_th = Thread(target=main_loop.create_task, args=(notifier(stopev),))
    handl_trasection_th = Thread(
        target=main_loop.create_task, args=(handl_trasection(stopev),)
    )
    auto_backup_proc = Thread(target=main_loop.create_task,args=[auto_backup.backup_process(stopev)])
    notifier_th.start()
    handl_trasection_th.start()
    auto_backup_proc.start()
    await idle()
    stopev.set()
    main_loop.stop()
    await app.stop()


main_loop = asyncio.get_event_loop()
main_loop.create_task(main())
main_loop.run_forever()
