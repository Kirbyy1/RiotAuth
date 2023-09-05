from collections import OrderedDict
from time import time

import RiotAuth.exceptions
from RiotAuth.captcha import solve_hcaptcha
from RiotAuth.session import undetected_request_session
from RiotAuth.utilities import Version, magic_decode, Token, User, RED_BLUE_ENDPOINTS

version = Version()

# Define constants
AUTHORIZATION = "https://auth.riotgames.com/api/v1/authorization"
AUTHENTICATE_URL = "https://authenticate.riotgames.com/api/v1/login"
LOGIN_TOKEN_URL = "https://authenticate.riotgames.com/api/v1/login"
LOGIN_TOKEN_API_URL = "https://auth.riotgames.com/api/v1/login-token"
USERINFO_URL = "https://auth.riotgames.com/userinfo"
CLIENT_ID = "riot-client"


class CaptchaFlow:
    def __init__(self, session, user):
        self.ses = session
        self.user = user

    def get_captcha_token(self):
        data = OrderedDict({
            "apple": None,
            "campaign": None,
            "clientId": CLIENT_ID,
            "code": None,
            "facebook": None,
            "gamecenter": None,
            "google": None,
            "language": "",
            "multifactor": None,
            "nintendo": None,
            "platform": "windows",
            "playstation": None,
            "remember": False,
            "riot_identity": {
                "campaign": None,
                "captcha": None,
                "language": "en_GB",
                "password": None,
                "remember": None,
                "state": "auth",
                "username": None
            },
            "riot_identity_signup": None,
            "rso": None,
            "sdkVersion": version.sdk,
            "type": "auth",
            "xbox": None
        })
        try:
            response = self.ses.post(AUTHENTICATE_URL, json=data)
            return response.json()
        except Exception as e:
            raise exceptions.UnableToRetrieveCaptchaToken(e) from e

    def get_login_token(self, code: str):
        data = OrderedDict({
            "riot_identity": {
                "campaign": None,
                "captcha": f"hcaptcha {code}",
                "language": "en_GB",
                "password": self.user.password,
                "remember": False,
                "username": self.user.username
            },
            "type": "auth"
        })
        try:
            response = self.ses.put(LOGIN_TOKEN_URL, json=data)

            return response.json()["success"]["login_token"]
        except Exception as e:
            raise exceptions.UnableToRetrieveLoginToken(e) from e

    def login_cookies(self, login_token: str):
        data = OrderedDict({
            "authentication_type": "RiotAuth",
            "code_verifier": "",
            "login_token": login_token,
            "persist_login": False
        })
        try:
            self.ses.post(LOGIN_TOKEN_API_URL, json=data)
        except Exception as e:
            raise exceptions.UnableToRetrieveLoginCookies(e) from e

    def captcha_flow(self):
        captcha_data = self.get_captcha_token()
        captcha_token = solve_hcaptcha(captcha_data)
        print(captcha_token)
        login_token = self.get_login_token(captcha_token)
        self.login_cookies(login_token)


def setup_auth(session):
    data = OrderedDict({
        "claims": "",
        "client_id": "riot-client",
        "nonce": "Yirb50C-j8x3rVzYAw61dw",
        "code_challenge": "",
        "code_challenge_method": "",
        "redirect_uri": "http://localhost/redirect",
        "response_type": "token id_token",
        "scope": "account openid",
    })

    return session.post(AUTHORIZATION, json=data)


def get_auth_data(session):
    r = setup_auth(session)
    cookies = dict(r.cookies)
    data = r.json()
    if "error" in data:
        raise Exception(data["error"])
    uri = data["response"]["parameters"]["uri"]
    token = get_token(uri)
    return token, cookies


def get_token(uri: str):
    access_token = uri.split("access_token=")[1].split("&scope")[0]
    token_id = uri.split("id_token=")[1].split("&")[0]
    expires_in = uri.split("expires_in=")[1].split("&")[0]
    timestamp = time() + float(expires_in)
    return Token(access_token, token_id, timestamp)


def get_user_info(session, token: Token):
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": f"Bearer {token.access_token}",
    }
    r = session.post(USERINFO_URL, headers=headers, json={})
    return magic_decode(r.text)


def authentication(username, password):
    session = undetected_request_session()
    setup_auth(session)

    user = User(username, password)
    flow = CaptchaFlow(session, user)
    flow.captcha_flow()

    token, cookies = get_auth_data(session)
    return get_user_info(session, token)


def get_wallet(access_token, user_info, session):
    URL = f"https://eune-red.lol.sgp.pvp.net/lolinventoryservice-ledge/v1/walletsbalances?puuid={user_info['sub']}&location=lolriot.aws-euc1-prod.eun1&accountId={user_info['lol_account']['summoner_id']}&currencyTypes=RP"

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/json",
        "Host": RED_BLUE_ENDPOINTS[str(user_info['region']['id']).upper()],
        "user-agent": "LeagueOfLegendsClient/13.17.528.2266 (rcp-be-lol-inventory)"
    }

    return session.get(URL, headers=headers)

