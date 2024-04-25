import requests
import time
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

def _send_file_tl(token, chat_id, filePath):
    url = f"https://api.telegram.org/bot{token}/sendDocument"

    files = {'document': open(filePath, 'rb')}

    data = {'chat_id': chat_id}

    response = requests.post(url, files=files, json=data)

    return response.json()

def backup_process():
    while True:
        backup()
        _send_file_tl(
            cohandler.config["bot"]["bot_token"],
            cohandler.config["bot"]["backup_channel"],
            "backup.gz"
        )
        time.sleep(300)