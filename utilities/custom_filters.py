import asyncio
import time
from pyrogram import filters
from pyrogram.errors.exceptions import (
    UserNotParticipant,
    UsernameNotOccupied,
    ChatAdminRequired,
)
from utilities.config_handler import *


cohandler = ConfigHandler()


message_timestamps = {}


async def Isspam(_, __, query):
    try:
        current_time = time.time()
        user_id = query.from_user.id
        if query.from_user.id not in message_timestamps.keys():
            message_timestamps[user_id] = []
        timestamps = message_timestamps[user_id]
        timestamps = [t for t in timestamps if current_time - t <= 60]
        timestamps.append(current_time)
        message_timestamps[user_id] = timestamps
        return len(timestamps) >= 30
    except AttributeError:
        return False


is_spamming = filters.create(Isspam)


def IsJoined(client):
    async def func(flt, _, query):
        userid = query.from_user.id
        channel = cohandler.config["bot"]["sponsor_channel"].replace(
            "https://t.me/", ""
        )
        if channel == False:
            return True
        try:
            user = await flt.client.get_chat_member(channel, userid)
            if user.user:
                return True
            else:
                return False
        except UserNotParticipant:
            return False
        except Exception as ex:
            logger(__name__).error(
                f"Chacking user join status \n User-id:{userid} \n Channel : {channel} \n error : {ex} "
            )
            return False

    return filters.create(func, client=client)


def dynamic_data_filter(data):
    async def func(flt, _, query):
        if ":" in query.data:
            return flt.data == query.data.split(":")[0]
        else:
            return flt.data == query.data

    return filters.create(func, data=data)


def IsAdmin(client):
    async def func(flt, _, query):
        try:
            userid = query.from_user.id
            admins = cohandler.config["bot"]["admin"]
            try:
                for admin in admins.split(","):
                    if admin.isdigit():
                        if int(admin) == userid:
                            return True
                        else:
                            continue
                    else:
                        if query.from_user.username.lower() == admin.lower():
                            return True
                        else:
                            continue
                else:
                    return False
            except Exception as ex:
                logger(__name__).error(
                    f"Chacking user admin status \n User-id:{userid} \n error : {ex} "
                )
                return False
        except AttributeError:
            return False

    return filters.create(func, client=client)
