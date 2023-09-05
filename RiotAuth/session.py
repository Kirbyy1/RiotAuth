# SSL ciphers to use when establishing SSL connection.
# https://en.wikipedia.org/wiki/Cipher_suite


import ssl
from collections import OrderedDict
from typing import Any

from requests import Session
from requests.adapters import HTTPAdapter

from RiotAuth.utilities import Version

CIPHERS = [
    "ECDHE-ECDSA-CHACHA20-POLY1305",
    "ECDHE-RSA-CHACHA20-POLY1305",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-RSA-AES128-GCM-SHA256",
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES128-SHA",
    "ECDHE-RSA-AES128-SHA",
    "ECDHE-ECDSA-AES256-SHA",
    "ECDHE-RSA-AES256-SHA",
    "AES128-GCM-SHA256",
    "AES256-GCM-SHA384",
    "AES128-SHA",
    "AES256-SHA",
    "DES-CBC3-SHA"
]


class SSLAdapter(HTTPAdapter):
    # Override the init_poolmanager method to set the SSL ciphers used for establishing SSL connections
    def init_poolmanager(self, *a: Any, **k: Any) -> None:
        # Create a default SSL context for server authentication
        c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        # Set the SSL ciphers to use
        c.set_ciphers(':'.join(CIPHERS))
        # Set the SSL context in the keyword arguments
        k['ssl_context'] = c
        # Call the superclass's init_poolmanager method
        return super(SSLAdapter, self).init_poolmanager(*a, **k)


def undetected_request_session():
    """
    Use the Ciphers module to bypass Cloudflare's protection and access the server.
    Cloudflare is a security and performance platform that protects websites from
    various types of attacks and provides caching and optimization services.
     The Ciphers module is used to decrypt the encrypted responses from the server,
      allowing the code to access the protected server.
    :return:
    """
    session = Session()

    app = "rso-auth"
    session.headers.update(OrderedDict({
        "User-Agent": f'RiotClient/{Version().riot} {app} (Windows;10;;Professional, x64)',
        "Cache-Control": "no-cache",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }))
    session.cookies.update({"tdid": "", "asid": "", "did": "", "clid": ""})
    session.mount('https://', SSLAdapter())

    return session
