import asyncio

from collections.abc import Callable

from pyrogram import Client

from clicker_api import ClickerApi


class BaseStrategy:
    """
    BaseStrategy class

    Attributes:
        strategy_name (str): name of the strategy
        pyrogram_client (Client): pyrogram client
        api (ClickerApi): clicker api
    """

    strategy_name: str
    pyrogram_client: Client
    api: ClickerApi

    def __init__(self, strategy_name: str, pyrogram_client: Client, api: ClickerApi):
        self.strategy_name = strategy_name
        self.pyrogram_client = pyrogram_client
        self.api = api

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Strategy({self.strategy_name} | {self.pyrogram_client.phone_number})"

    async def auth(self) -> None:
        """
        Auth method
        """

        await self.pyrogram_client.start()

    async def base_setup(self) -> None:  # , profile_photo: io.BytesIO) -> None:
        """
        Base setup method
        """
        raise NotImplementedError

    async def update_webapp_session(self) -> str:
        """
        Update webapp method
        """
        raise NotImplementedError

    @staticmethod
    async def periodic_task(task: Callable, sleep_time: float, sleep_before: bool = False) -> None:
        """
        Periodic task method
        """
        while True:
            if sleep_before:
                await asyncio.sleep(sleep_time)
            await task()
            if not sleep_before:
                await asyncio.sleep(sleep_time)

    async def run_strategy(self) -> None:
        """
        Run method
        """
        raise NotImplementedError
