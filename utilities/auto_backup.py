import aiohttp
import asyncio
import os

from enums.datebaseenums import database
from utilities.config_handler import ConfigHandler


cohandler = ConfigHandler()

def backup():
    command = "mongodump --db {} --gzip --archive > backup.gz".format(database.dateBaseName)
    os.system(command)

def restore_backup(name:str):
    command = "mongorestore --gzip --archive={}".format(name)
    os.system(command)

async def _send_file_tl(token, chat_id, filePath):

  url = f"https://api.telegram.org/bot{token}/sendDocument"

  async with aiohttp.ClientSession() as session:

    files = {'document': open(filePath, 'rb')}

    data = {'chat_id': chat_id}

    async with session.post(url, file=files, data=data) as response:
      return await response.json()

async def backup_process(stop_event):
    while not stop_event.is_set():
        backup()
        await _send_file_tl(
            cohandler.config["bot"]["bot_token"],
            cohandler.config["bot"]["backup_channel"],
            "backup.gz"
        )
        await asyncio.sleep(300)