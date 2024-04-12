import base64
import ssl

from typing import ClassVar

from aiohttp import TCPConnector

# from asyncio import BaseTransport
# from trace import Trace
# from aiohttp import ClientConnectionError, ClientRequest, ClientTimeout
# from aiohttp.client_proto import ResponseHandler
# from socks import SOCKSServerError, open_socks_connection
from aiohttp_proxy import ProxyConnector
from pythonmonkey import eval as js_eval

from tests.cloudflare_bypass.main import BypassTLS


def calculate_hash(hashes: list[str], telegram_user_id: int) -> int:
    """
    Calculate hash method
    """

    functions = [f"({base64.b64decode(string).decode("utf-8")})" for string in hashes]
    function = " + ".join(functions)

    return int(
        js_eval(f"""
        window = {{
            location: {{ host: "clicker.joincommunity.xyz" }},
            Telegram: {{
                WebApp: {{
                    initDataUnsafe: {{
                        user: {{ id: {telegram_user_id} }}
                    }}
                }}
            }}
        }};
        document = {{
            querySelectorAll: (_) => {{ return "1" }}
        }};
        {function}
        """)
    )


class BypassTLSProxy(BypassTLS, ProxyConnector):
    ...


class BypassTLS(TCPConnector):
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
        # "TLS_AES_128_CCM_SHA256",
        # "TLS_AES_256_CCM_8_SHA256",
    ]

    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.set_ciphers(":".join(BypassTLSProxy.SUPPORTED_CIPHERS))
        self.ssl_context.set_ecdh_curve("prime256v1")
        self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        super().__init__(*args, ssl=self.ssl_context, **kwargs)

    # async def _create_proxy_connection(
    #     self, req: "ClientRequest", traces: list["Trace"], timeout: "ClientTimeout"
    # ) -> tuple[BaseTransport, ResponseHandler]:
    #     if req.proxy is None:
    #         raise RuntimeError("empty proxy URL")
    #     if req.proxy.scheme == "socks5":
    #         try:
    #             if req.port is not None:
    #                 transport = await open_socks_connection(req.proxy, req.host, req.port)
    #             elif req.url.scheme == "http":
    #                 transport = await open_socks_connection(req.proxy, req.host, 80)
    #             elif req.url.scheme == "https":
    #                 transport = await open_socks_connection(req.proxy, req.host, 443)
    #             else:
    #                 raise RuntimeError(f"unexpected URL scheme: {req.url.scheme}")
    #         except (SOCKSServerError, ConnectionError) as e:
    #             raise ClientConnectionError("SOCKS connection failed") from e
    #         if req.is_ssl():
    #             return await self._start_tls_connection(transport, req=req, timeout=timeout)
    #         proto = ResponseHandler(self._loop)
    #         proto.connection_made(transport)
    #         return transport, proto
    #
    #     return await super()._create_proxy_connection(req, traces, timeout)
