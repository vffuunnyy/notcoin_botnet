import contextlib

from typing import ClassVar

from aiohttp import ClientSession

from proxy_client import ProxyClient
from src.helpers import BypassTLSProxy
from src.models.requests import ClickRequest, PlausibleEventRequest, WebAppSessionRequest
from src.models.responses import (
    ActiveTurboData,
    BaseClickerData,
    BaseResponse,
    CheckTurboData,
    ClickData,
    CompletedTaskData,
    ExceptionData,
    ProfileData,
    ShopItemData,
    WebAppSessionData,
)


class ClickerApi:
    PLAUSIBLE_URL = "https://plausible.joincommunity.xyz/api/event"
    API_URL = "https://clicker-api.joincommunity.xyz"

    http_client: ClientSession
    proxy: str
    base_headers: ClassVar[dict[str, str]] = {
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Android WebView";v="120"',
        "DNT": "1",
        "Sec-Ch-Ua-Mobile": "?1",
        "Accept": "application/json",
        "Referer": "https://clicker.joincommunity.xyz/",
        "Sec-Ch-Ua-Platform": '"Android"',
        "X-Requested-With": "org.telegram.messenger.web",
    }
    options_headers: ClassVar[dict[str, str]] = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7",
        "Access-Control-Request-Headers": "auth,authorization",
        # "Access-Control-Request-Method": "GET",
        "Cache-Control": "no-cache",
        "Referer": "https://clicker.joincommunity.xyz/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-Requested-With": "org.telegram.messenger.web",
    }
    webapp_session: str
    bearer: str | None = None

    last_clicker_data: ClickData | None = None
    last_profile_data: ProfileData | None = None

    auth_header_value = "6"

    def __init__(self, proxy: str, device_model: str):
        self.proxy = proxy
        self.base_headers["User-Agent"] = self.options_headers["User-Agent"] = (
            f"Mozilla/5.0 (Linux; Android 12; {device_model} Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.193 Mobile Safari/537.36"
        )
        self.proxy_client = ProxyClient()
        self.http_client = ClientSession(connector=BypassTLSProxy.from_url(self.proxy_client.get_proxy()))

    async def get(
        self, url: str, params: dict | None = None, auth: bool = False, options: bool = True
    ) -> tuple[int, str]:
        """
        Get method
        """

        headers = self.base_headers.copy()
        options_headers = self.options_headers.copy()

        if auth:
            headers["Auth"] = self.auth_header_value
            headers["Authorization"] = "Bearer " + self.bearer

        if options:
            options_headers["Access-Control-Request-Method"] = "GET"
            await self.options(url, options_headers)

        try:
            async with self.http_client.get(
                url, params=params, skip_auto_headers=["Content-Type"], headers=headers
            ) as response:
                return response.status, await response.text()
        except:
            await self.http_client.close()
            self.http_client = ClientSession(connector=BypassTLSProxy.from_url(self.proxy_client.get_proxy()))
            return await self.get(url, params=params, auth=auth, options=options)

    async def post(
        self, url: str, data: dict | None = None, auth: bool = False, options: bool = True
    ) -> tuple[int, str]:
        """
        Post method

        """

        headers = self.base_headers.copy()
        options_headers = self.options_headers.copy()

        if auth:
            headers["Auth"] = self.auth_header_value
            headers["Authorization"] = "Bearer " + self.bearer

        if data:
            headers["Content-Type"] = "application/json"
            options_headers["Access-Control-Request-Headers"] += ",content-type"

        if options:
            options_headers["Access-Control-Request-Method"] = "GET"
            await self.options(url, options_headers)

        try:
            async with self.http_client.post(
                url, json=data, skip_auto_headers=["Content-Type"], headers=headers
            ) as response:
                return response.status, await response.text()
        except:
            await self.http_client.close()
            self.http_client = ClientSession(connector=BypassTLSProxy.from_url(self.proxy_client.get_proxy()))
            return await self.post(url, data=data, auth=auth, options=options)

    async def options(self, url: str, headers: dict[str, str]) -> int:
        """
        Options method
        """

        with contextlib.suppress(Exception):
            async with self.http_client.options(url, headers=headers, skip_auto_headers=["Content-Type"]) as response:
                return response.status

    async def api_get(self, url: str, params: dict | None = None, auth: bool = True) -> BaseResponse | ExceptionData:
        """
        Api get method
        """
        status_code, response = await self.get(url, params=params, auth=auth)

        while '<!DOCTYPE html><html lang="en-US">' in response:
            await self.http_client.close()
            self.http_client = ClientSession(connector=BypassTLSProxy.from_url(self.proxy_client.get_proxy()))
            status_code, response = await self.get(url, params=params, auth=auth)

        response = BaseResponse.model_validate_json(response)

        if status_code >= 400:
            return ExceptionData.model_validate(response.data)

        return response

    async def api_post(self, url: str, data: dict | None = None, auth: bool = True) -> BaseResponse | ExceptionData:
        """
        Api post method
        """
        status_code, response = await self.post(url, data=data, auth=auth)

        while '<!DOCTYPE html><html lang="en-US">' in response:
            await self.http_client.close()
            self.http_client = ClientSession(connector=BypassTLSProxy.from_url(self.proxy_client.get_proxy()))
            status_code, response = await self.post(url, data=data, auth=auth)

        response = BaseResponse.model_validate_json(response)

        if status_code >= 400:
            return ExceptionData.model_validate(response.data)

        return response

    async def send_plausible_event(self, event: PlausibleEventRequest) -> None:
        """
        Send plausible event method
        """
        await self.post(self.PLAUSIBLE_URL, data=event.model_dump(by_alias=True, exclude_none=True), options=False)

    async def webapp_auth_session(self, webapp_session: WebAppSessionRequest) -> None:
        """
        Webapp auth session method
        """
        self.webapp_session = webapp_session.web_app_data

        await self.send_plausible_event(
            PlausibleEventRequest(
                url=f"https://clicker.joincommunity.xyz/clicker#{webapp_session.web_app_data}",
            )
        )

        response = await self.api_post(
            f"{self.API_URL}/auth/webapp-session",
            data=webapp_session.model_dump(by_alias=True, exclude_none=True),
            auth=False,
        )

        if isinstance(response, ExceptionData):
            raise Exception(response.message)

        response = WebAppSessionData.model_validate(response.data)
        self.bearer = response.access_token

    async def get_profile(self) -> ProfileData | ExceptionData:
        """
        Get profile method
        """

        response = await self.api_get(f"{self.API_URL}/clicker/profile")

        if isinstance(response, ExceptionData):
            return response

        model = ProfileData.model_validate(response.data[0])

        self.last_profile_data = model

        return model

    async def get_shop(self) -> list[ShopItemData] | ExceptionData:
        """
        Get shop method
        """

        await self.send_plausible_event(
            PlausibleEventRequest(
                url="https://clicker.joincommunity.xyz/clicker/boosts",
            )
        )

        response = await self.api_get(f"{self.API_URL}/clicker/store/merged")

        if isinstance(response, ExceptionData):
            return response

        return [ShopItemData.model_validate(item) for item in response.data]

    async def claim_shop_item(self, item_id: int) -> BaseClickerData | ExceptionData:
        """
        Claim shop item method
        """

        response = await self.api_post(f"{self.API_URL}/clicker/store/buy/{item_id}")

        if isinstance(response, ExceptionData):
            return response

        model = BaseClickerData.model_validate(response.data)

        self.last_profile_data.multiple_clicks = model.multiple_clicks
        self.last_profile_data.recharging_speed = model.recharging_speed
        self.last_profile_data.energy_limit = model.energy_limit
        self.last_profile_data.with_robot = model.with_robot
        self.last_profile_data.balance = model.balance

        return model

    async def get_completed_tasks(self) -> list[CompletedTaskData] | ExceptionData:
        """
        Get completed tasks method
        """

        await self.send_plausible_event(
            PlausibleEventRequest(
                url="https://clicker.joincommunity.xyz/clicker/earn",
            )
        )

        response = await self.api_get(f"{self.API_URL}/clicker/task/combine-completed")

        if isinstance(response, ExceptionData):
            return response

        return [CompletedTaskData.model_validate(item) for item in response.data]

    async def claim_completed_task(self, task_id: int) -> BaseClickerData | ExceptionData:
        """
        Claim completed task method
        """

        response = await self.api_post(f"{self.API_URL}/clicker/task/{task_id}")

        if isinstance(response, ExceptionData):
            return response

        model = BaseClickerData.model_validate(response.data)

        self.last_profile_data.balance = model.balance
        self.last_profile_data.total_coins = model.total_coins
        self.last_profile_data.available_energy = model.available_energy
        self.last_profile_data.turbo_times = model.turbo_times

        return model

    async def check_robot(self) -> int | ExceptionData:
        """
        Check robot method
        """

        response = await self.api_get(f"{self.API_URL}/clicker/core/robot")

        if isinstance(response, ExceptionData):
            return response

        return response.data

    async def claim_robot(self) -> BaseClickerData | ExceptionData:
        """
        Claim robot method
        """

        response = await self.api_post(f"{self.API_URL}/clicker/core/robot")

        if isinstance(response, ExceptionData):
            return response

        model = BaseClickerData.model_validate(response.data)

        self.last_profile_data.balance = model.balance
        self.last_profile_data.total_coins = model.total_coins

        return model

    async def check_turbo(self) -> bool | ExceptionData:
        """
        Check turbo method
        """

        response = await self.api_post(f"{self.API_URL}/clicker/core/check-turbo")

        if isinstance(response, ExceptionData):
            return response

        return CheckTurboData.model_validate(response.data).turbo

    async def activate_turbo(self) -> ActiveTurboData | ExceptionData:
        """
        Activate turbo method
        """

        response = await self.api_post(f"{self.API_URL}/clicker/core/active-turbo")

        if isinstance(response, ExceptionData):
            return response

        return ActiveTurboData.model_validate(response.data[0])

    async def click(self, click_request: ClickRequest) -> ClickData | ExceptionData:
        """
        Click method
        """

        response = await self.api_post(
            f"{self.API_URL}/clicker/core/click",
            data=click_request.model_dump(by_alias=True, exclude_none=True),
        )

        if isinstance(response, ExceptionData):
            return response

        model = ClickData.model_validate(response.data[0])

        self.last_clicker_data = model
        self.last_profile_data.balance = model.balance
        self.last_profile_data.total_coins = model.total_coins

        return model
