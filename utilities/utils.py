from base64 import b64encode, b64decode
from json import loads, dumps
from urllib.parse import quote
from utilities.config_handler import ConfigHandler


cohandler = ConfigHandler()


def change_service_name(name: str, flag: str):
    custom_name = cohandler.config["bot"]["custom_name"]
    return f"{custom_name} ({flag} {name})"


def change_config_name(config: str, name: str, flag: str):
    if config.startswith("vmess://"):
        config_data = loads(
            b64decode(
                config.split("vmess://")[1],
            ).decode()
        )

        config_data["ps"] = change_service_name(name, flag)

        return "vmess://{}".format(b64encode(dumps(config_data).encode()).decode())

    elif config.startswith("vless://"):
        _config = config.split("#")[0]

        config = f"{_config}#{quote(change_service_name(name, flag))}"

        return config