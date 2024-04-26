import configparser
from os import mkdir
from os.path import exists
from logging import basicConfig, StreamHandler, INFO, Logger, getLogger
from logging.handlers import RotatingFileHandler
from datetime import datetime


class ConfigHandler:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def getconfig(self):
        self.config.read("config.ini", encoding="utf-8")
        return self.config

    def update_config(self, section, option, value):
        self.config.read("config.ini", encoding="utf-8")
        self.config.set(section, option, value)
        with open("config.ini", "w", encoding="utf-8") as con:
            self.config.write(con)


if not exists("./logs"):
    mkdir("logs")

file_name = f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

basicConfig(
    level=INFO,
    format="[%(asctime)s - %(levelname)s] : %(name)s ~> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RotatingFileHandler(file_name, maxBytes=1_000_000_000, backupCount=5),
        StreamHandler(),
    ],
)


def logger(name: str = __name__) -> Logger:
    return getLogger(name)
