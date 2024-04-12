"""
:authority:clicker-api.joincommunity.xyz
:method:POST
:path:/clicker/core/click
:scheme:https
Accept:application/json
Accept-Encoding:gzip, deflate, br
Accept-Language:en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7
Auth:5
Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyNjIzODIwLCJleHBpcmUiOjE3MDU2Njk0OTkxNTIsImlhdCI6MTcwNTY0Nzg5OSwiZXhwIjoxNzEzNDIzODk5fQ.3gEXMa9Y-5kzaE622E-WevU3pHzuIIaEIz4SjFC44YQ
Cache-Control:no-cache
Content-Length:370
Content-Type:application/json
Origin:https://clicker.joincommunity.xyz
Pragma:no-cache
Referer:https://clicker.joincommunity.xyz/
Sec-Ch-Ua:"Not_A Brand";v="8", "Chromium";v="120", "Android WebView";v="120"
Sec-Ch-Ua-Mobile:?1
Sec-Ch-Ua-Platform:"Android"
Sec-Fetch-Dest:empty
Sec-Fetch-Mode:cors
Sec-Fetch-Site:same-site
User-Agent: Mozilla/5.0 (Linux; Android 12; M2007J3SY Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.210 Mobile Safari/537.36
X-Requested-With: org.telegram.messenger.web
"""

import asyncio
import ssl
from typing import ClassVar

import aiohttp

from aiohttp import ClientSession


base_headers: dict[str, str] = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7",
    "Auth": "5",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjk4Nzg3NTcsImV4cGlyZSI6MTcwNTcyMjQ1Njc3MCwiaWF0IjoxNzA1NzAwODU2LCJleHAiOjE3MTM0NzY4NTZ9.PVnNT7JL3BTVsekUWu1TFhOVmTAWJDt-yU5CD1Nb8Qk",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "Origin": "https://clicker.joincommunity.xyz",
    "Pragma": "no-cache",
    "Referer": "https://clicker.joincommunity.xyz/",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Android WebView";v="120"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; X670E Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.193 Mobile Safari/537.36",
    "X-Requested-With": "org.telegram.messenger.web",
}

data = {
    "webAppData": "query_id=AAFzpXcgAwAAAHOldyCu2Qb9&user=%7B%22id%22%3A6987162995%2C%22first_name%22%3A%22Nicole%22%2C%22last_name%22%3A%22King%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1705700835&hash=935600681026c2c023d2d048bda64cef00cee4603e4cd1a5bad2fe91d1a350c7",
    "count": 4,
}


class BypassTLS(aiohttp.TCPConnector):
    SUPPORTED_CIPHERS: ClassVar[list[str]] = [
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305",
        "ECDHE-RSA-AES128-SHA",
        "ECDHE-RSA-AES256-SHA",
        "AES128-GCM-SHA256",
        "AES256-GCM-SHA384",
        "AES128-SHA",
        "AES256-SHA",
        "DES-CBC3-SHA",
        "TLS_AES_128_GCM_SHA256",
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_CCM_SHA256",
        "TLS_AES_256_CCM_8_SHA256",
    ]

    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.set_ciphers(":".join(BypassTLS.SUPPORTED_CIPHERS))
        self.ssl_context.set_ecdh_curve("prime256v1")
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        super().__init__(*args, ssl=self.ssl_context, **kwargs)


async def post(url: str) -> None:
    """
    Post method

    """

    async with (
        ClientSession(connector=BypassTLS()) as http_client,
        http_client.post(url, json=data, headers=base_headers) as response,
    ):
        print(response.status, await response.text())


asyncio.run(post("https://clicker-api.joincommunity.xyz/clicker/core/click"))
