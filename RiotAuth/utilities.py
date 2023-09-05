import contextlib
import json
from dataclasses import dataclass
from time import time

import jwt
import requests

RED_BLUE_ENDPOINTS = {
    "BR1": "br-red.lol.sgp.pvp.net",
    "EUN1": "eune-blue.lol.sgp.pvp.net",
    "EUW1": "euw-blue.lol.sgp.pvp.net",
    "JP1": "jp-red.lol.sgp.pvp.net",
    "LA1": "lan-red.lol.sgp.pvp.net",
    "LA2": "las-red.lol.sgp.pvp.net",
    "NA1": "na-red.lol.sgp.pvp.net",
    "OC1": "oce-red.lol.sgp.pvp.net",
    "RU": "ru-blue.lol.sgp.pvp.net",
    "TR1": "tr-blue.lol.sgp.pvp.net",
    "KR": "kr-red.lol.sgp.pvp.net",
    'PH2': "ph2-red.lol.sgp.pvp.net",
    'SG2': "sg",
    'TH2': "th",
    'TW2': "tw2-red.lol.sgp.pvp.net",
    'VN2': "vn"
}


def magic_decode(string: str):
    with contextlib.suppress(json.JSONDecodeError):
        return json.loads(string)
    with contextlib.suppress(jwt.exceptions.DecodeError):
        return jwt.decode(string, options={"verify_signature": False})
    raise Exception


@dataclass
class Token():
    access_token: str
    id_token: str
    expire: float
    created = time()


class Version:
    def __init__(self):
        self.versions = requests.get("https://valorant-api.com/v1/version").json()["data"]
        self.riot = self.riot()
        self.sdk = self.sdk()

    def riot(self):
        return self.versions["riotClientBuild"]

    def sdk(self):
        return sdk if (sdk := self.versions["riotClientVersion"].split(".")[1]) else "23.8.0.1382"


@dataclass
class User:
    username: str = ''
    password: str = ''

    def __hash__(self):
        return hash(self.username)
