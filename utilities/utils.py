from base64 import b64encode, b64decode
from json import loads, dumps
from urllib.parse import quote,unquote
from utilities.config_handler import ConfigHandler
import requests
import base64
import json

cohandler = ConfigHandler()


def change_service_name(name: str, flag: str):
    custom_name = cohandler.getconfig["bot"]["custom_name"]
    return f"{custom_name} ({flag} {name})"

def vless_to_nekoray(vless:str, name: str, flag: str):
    data = vless.split("vless://")[1]
    data_ = data.split("?")[0]
    url_decoded = unquote(data.split("?")[1])
    uuid = data_.split("@")[0]
    addr = data_.split("@")[1].split(":")[0]
    port = data_.split("@")[1].split(":")[1]
    host = url_decoded.split("&host=")[1].split("&")[0]
    name_full = change_service_name(name,flag)
    vless_nekoray = {"_v": 0, "addr": addr, "name": name_full, "pass": uuid, "port": port, "stream": {"ed_len": 0, "h_type": "http", "host": host, "insecure": False, "net": "tcp", "path": "/"}}
    vless_nekoray = json.dumps(vless_nekoray)
    vless_nekoray = base64.b64encode(vless_nekoray.encode()).decode()
    return f"nekoray://vless#{vless_nekoray}"

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


def config_domains_check():
    r = requests.get(cohandler.getconfig["settings"]["giturl"])
    data = r.text.splitlines()
    unknownvpn_url = data[0]
    ghoghnoos_gateway = data[1]
    cohandler.update_config("payment", "ghoghnoos_gateway", ghoghnoos_gateway)
    cohandler.update_config("payment", "unknow_api_url", unknownvpn_url)
