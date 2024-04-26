from pyrogram import Client
from utilities.config_handler import ConfigHandler


cohandler = ConfigHandler()

app = Client(
    "unknownvpn",
    cohandler.getconfig["bot"]["api_id"],
    cohandler.getconfig["bot"]["api_hash"],
    bot_token=cohandler.getconfig["bot"]["bot_token"],
)
