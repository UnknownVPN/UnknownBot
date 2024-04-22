from pyrogram import Client
from utilities.config_handler import ConfigHandler


cohandler = ConfigHandler()

app = Client(
    "unknownvpn",
    cohandler.config["bot"]["api_id"],
    cohandler.config["bot"]["api_hash"],
    bot_token=cohandler.config["bot"]["bot_token"],
)
