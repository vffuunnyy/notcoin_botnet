import asyncio
import logging
import math
import re
import urllib.parse

import arrow

from aiohttp_proxy.helpers import parse_proxy_url
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import UserDeactivatedBan
from pyrogram.raw import functions
from pyrogram.raw.types import DataJSON

from src.base_strategy import BaseStrategy
from src.clicker_api import ClickerApi
from src.helpers import calculate_hash
from src.models.requests import ClickRequest, PlausibleEventRequest, WebAppSessionRequest
from src.models.responses import ExceptionData, ShopItemData


class StandardStrategy(BaseStrategy):
    logger_username: str = "@vffuunnyy"
    notcoin_username: str = "@notcoin_bot"
    referral_command: str = "/start r_577708_12623820"

    SLEEP_BETWEEN_BOOSTERS: int = 4
    SLEEP_BETWEEN_CLICKS: int = 10

    ENERGY_LIMIT_MAX_LEVEL: int = 10000
    RECHARGING_SPEED_MAX_LEVEL: int = 3
    MULTIPLE_CLICKS_MAX_LEVEL: int = 3

    earning_per_loop = 0

    def __init__(self, strategy_name: str, pyrogram_client: Client, proxy: str | None = None):
        super().__init__(strategy_name, pyrogram_client, ClickerApi(proxy, pyrogram_client.device_model))

        self.background_tasks = set()

    async def base_setup(self) -> None:  # , profile_photo: io.BytesIO) -> None:
        """
        Setup method
        """
        self.pyrogram_client.set_parse_mode(ParseMode.HTML)

        # await self.auth()
        #
        # self.pyrogram_client.me = await self.pyrogram_client.get_me()
        # self.pyrogram_client.set_parse_mode(ParseMode.HTML)

        # await asyncio.sleep(5)

        # await self.pyrogram_client.set_profile_photo(photo=profile_photo)

        # await asyncio.sleep(5)
        #
        # await self.pyrogram_client.send_message(
        #     self.logger_username, f"{self.strategy_name}\nAuth success"
        # )

        # await asyncio.sleep(5)

        # self.background_tasks.add(
        #     task := self.pyrogram_client.loop.create_task(self.periodic_task(self.update_webapp_session, 60 * 60 * 1.5))
        # )
        # task.add_done_callback(self.background_tasks.discard)
        # self.background_tasks.add(
        #     task := self.pyrogram_client.loop.create_task(self.periodic_task(self.log_statistics, 60 * 10, True))
        # )
        # task.add_done_callback(self.background_tasks.discard)

    async def update_webapp_session(self) -> None:
        proxy_type, host, port, username, password = parse_proxy_url(self.api.proxy_client.get_proxy())

        self.pyrogram_client.proxy = {
            "scheme": str(proxy_type),
            "hostname": host,
            "port": port,
            "username": username,
            "password": password,
        }
        try:
            # await self.auth()
            async with asyncio.timeout(30):
                await self.pyrogram_client.start()
        except (TimeoutError, ConnectionError):
            logging.error("[%s] Proxy is dead", self.pyrogram_client.name)
            return await self.update_webapp_session()

        try:
            self.pyrogram_client.me = await self.pyrogram_client.get_me()

            await self.pyrogram_client.send_message(self.notcoin_username, self.referral_command)
            await asyncio.sleep(5)

            result = await self.pyrogram_client.invoke(
                functions.messages.request_web_view.RequestWebView(
                    peer=await self.pyrogram_client.resolve_peer(self.notcoin_username),
                    bot=await self.pyrogram_client.resolve_peer(self.notcoin_username),
                    platform="android",
                    from_bot_menu=False,
                    silent=False,
                    url="https://clicker.joincommunity.xyz/clicker",
                    start_param=None,
                    theme_params=DataJSON(
                        data="""{"bg_color":"#212d3b","section_bg_color":"#1d2733","secondary_bg_color":"#151e27","text_color":"#ffffff","hint_color":"#7d8b99","link_color":"#5eabe1","button_color":"#50a8eb","button_text_color":"#ffffff","header_bg_color":"#242d39","accent_text_color":"#64b5ef","section_header_text_color":"#79c4fc","subtitle_text_color":"#7b8790","destructive_text_color":"#ee686f"}"""
                    ),
                    reply_to=None,
                    send_as=None,
                )
            )

            result.url = urllib.parse.unquote(result.url)
            query_id_param = re.search("query_id=(.*?)&", result.url)
            user_param = re.search("user=(.*?)&", result.url)
            hash_param = re.search("hash=(.*?)&", result.url)
            auth_date_param = re.search("auth_date=(.*?)&", result.url)

            query_id = query_id_param.group(1) if query_id_param else None
            user = user_param.group(1) if user_param else None
            data_hash = hash_param.group(1) if hash_param else None
            auth_date = auth_date_param.group(1) if auth_date_param else None

            await self.api.webapp_auth_session(
                WebAppSessionRequest(
                    web_app_data=f"query_id={query_id}&user={user}&auth_date={auth_date}&hash={data_hash}"
                )
            )
        finally:
            await self.pyrogram_client.stop()

    async def log_statistics(self) -> None:
        """
        Log statistics method
        """

        if self.api.last_clicker_data:
            # await self.pyrogram_client.send_message(
            #     self.logger_username,
            log_string = (
                f"\n┏{self.strategy_name} - {self.pyrogram_client.me.first_name}\n"
                f"{
                f"┗❌ BOT BANNED: {self.api.last_profile_data.user.deleted_at.humanize()}\n"
                if self.api.last_profile_data.user.deleted_at or self.api.last_profile_data.user.is_blocked else
                "┗✅ BOT IS ACTIVE\n"
                }"
                "\n"
                f"┏Total Coins: {self.api.last_clicker_data.total_coins}\n"
                f"┣Balance: {self.api.last_clicker_data.balance}\n"
                f"┗Earning per loop: {self.earning_per_loop}\n"
                "\n"
                f"┏Multiple Clicks: {self.api.last_clicker_data.multiple_clicks}\n"
                f"┣Recharging Speed: {self.api.last_clicker_data.recharging_speed}\n"
                f"┣Energy Limit: {self.api.last_clicker_data.energy_limit}\n"
                f"┗🤖 Robot{" " if self.api.last_clicker_data.with_robot else " Not "}Equipped\n"
                "\n"
                f"Created At: {self.api.last_clicker_data.created_at.humanize()}\n"
            )
            # )

            logging.info(log_string)

    async def buy_booster_while_possible(self, item: ShopItemData, max_booster_level: int) -> int:
        """
        Buy booster while possible method
        """

        if self.api.last_profile_data.league_id < item.min_league_id:
            return 0

        start_count = item.count
        while item.count < max_booster_level and self.api.last_profile_data.balance >= item.price:
            logging.info(
                "[%s] Buying booster %s (%s), Price: %s",
                self.pyrogram_client.me.first_name,
                item.id,
                item.name,
                item.price,
            )

            response = await self.api.claim_shop_item(item.id)
            await asyncio.sleep(self.SLEEP_BETWEEN_BOOSTERS)

            if isinstance(response, ExceptionData):
                return item.count - start_count

            item.count += 1

        return item.count - start_count

    async def buy_available_boosters(self) -> int:
        """
        Buy available boosters method
        """

        shop = await self.api.get_shop()

        if isinstance(shop, ExceptionData):
            return 0

        await asyncio.sleep(self.SLEEP_BETWEEN_BOOSTERS)

        claimed_count = 0
        for item in shop:
            match item.id:
                case 1:  # Energy Limit
                    claimed_count += await self.buy_booster_while_possible(item, self.ENERGY_LIMIT_MAX_LEVEL)
                case 2:  # Recharging Speed
                    claimed_count += await self.buy_booster_while_possible(item, self.RECHARGING_SPEED_MAX_LEVEL)
                case 3:  # Multiple Clicks
                    claimed_count += await self.buy_booster_while_possible(item, self.MULTIPLE_CLICKS_MAX_LEVEL)
                case 18:  # Robot
                    claimed_count += await self.buy_booster_while_possible(item, 1)

        await self.api.send_plausible_event(
            PlausibleEventRequest(
                url="https://clicker.joincommunity.xyz/clicker",
            )
        )

        return claimed_count

    async def claim_task(self, task_id: int) -> None:
        """
        Claim task method
        """

        await self.api.claim_completed_task(task_id)
        logging.info("[%s] Claimed task %s", self.pyrogram_client.me.first_name, task_id)
        await asyncio.sleep(self.SLEEP_BETWEEN_BOOSTERS)

    async def claim_available_tasks(self) -> list[int]:
        """
        Claim available tasks method
        """

        # 2,  # Recover full energy
        # 3,  # Claim free turbo
        # 5,  # Get bonus for 10 referrals,

        BONUS_FOR_FIRST_1000_CLICKS = 4
        BONUS_FOR_JOINSQUAD = 6
        BONUS_FOR_SILVER_LEAGUE = 7
        BONUS_FOR_GOLD_LEAGUE = 8
        BONUS_FOR_PLATINUM_LEAGUE = 9

        tasks = await self.api.get_completed_tasks()
        completed_tasks = [task.task_id for task in tasks]

        if isinstance(tasks, ExceptionData):
            return []

        await asyncio.sleep(self.SLEEP_BETWEEN_BOOSTERS)

        if BONUS_FOR_FIRST_1000_CLICKS not in completed_tasks and self.api.last_profile_data.total_coins > 10000:
            await self.claim_task(BONUS_FOR_FIRST_1000_CLICKS)

        if BONUS_FOR_JOINSQUAD not in completed_tasks and self.api.last_profile_data.total_coins > 1000:
            await self.claim_task(BONUS_FOR_JOINSQUAD)

        if BONUS_FOR_SILVER_LEAGUE not in completed_tasks and self.api.last_profile_data.total_coins > 125000:
            await self.claim_task(BONUS_FOR_SILVER_LEAGUE)

        if BONUS_FOR_GOLD_LEAGUE not in completed_tasks and self.api.last_profile_data.total_coins > 250000:
            await self.claim_task(BONUS_FOR_GOLD_LEAGUE)

        if BONUS_FOR_PLATINUM_LEAGUE not in completed_tasks and self.api.last_profile_data.total_coins > 500000:
            await self.claim_task(BONUS_FOR_PLATINUM_LEAGUE)

        await self.api.send_plausible_event(
            PlausibleEventRequest(
                url="https://clicker.joincommunity.xyz/clicker",
            )
        )

        return completed_tasks

    async def run_clicker(self) -> None:
        completed_tasks = await self.claim_available_tasks()
        await self.buy_available_boosters()

        # TODO @vffuunnyy: turbo activation

        clicks_to_full_mine = self.api.last_profile_data.energy_limit / self.api.last_profile_data.multiple_clicks
        requests_count = math.ceil(clicks_to_full_mine / 159) + 1

        logging.info(
            "[%s] Clicks to full mine: %s, Requests count: %s",
            self.pyrogram_client.me.first_name,
            clicks_to_full_mine,
            requests_count,
        )

        for _ in range(requests_count):
            await self.api.click(
                ClickRequest(
                    web_app_data=self.api.webapp_session,
                    count=min(
                        self.api.last_profile_data.available_energy,
                        159 * self.api.last_profile_data.multiple_clicks,
                    ),
                    hash=calculate_hash(self.api.last_clicker_data.hash, self.pyrogram_client.me.id)
                    if self.api.last_clicker_data
                    else None,
                )
            )

            await asyncio.sleep(self.SLEEP_BETWEEN_CLICKS)

        if completed_tasks.count(2) < 3:  # Recover full energy
            logging.info("[%s] Claiming Recover full energy", self.pyrogram_client.me.first_name)

            await self.api.claim_completed_task(2)
            await self.api.send_plausible_event(
                PlausibleEventRequest(
                    url="https://clicker.joincommunity.xyz/clicker",
                )
            )
            await asyncio.sleep(self.SLEEP_BETWEEN_BOOSTERS)
            await self.run_clicker()

    async def run_strategy(self) -> None:
        """
        Run method
        """

        last_update_time = arrow.now().shift(hours=-2)
        while True:
            if (arrow.now() - last_update_time).seconds > 60 * 60 * 1.5:
                logging.info("[%s] Updating webapp session", self.pyrogram_client.name)

                try:
                    await self.update_webapp_session()
                except UserDeactivatedBan:
                    logging.error("[%s] Bot is banned", self.pyrogram_client.name)
                    return

                last_update_time = arrow.now()

            await self.api.get_profile()

            last_total = self.api.last_profile_data.total_coins

            logging.info(
                "[%s] Total coins: %s, Earning per loop: %s",
                self.pyrogram_client.me.first_name,
                self.api.last_profile_data.total_coins,
                self.earning_per_loop,
            )

            if self.api.last_profile_data.with_robot:
                bot_receive_timeout = 60 * 62 - (arrow.now() - self.api.last_profile_data.last_click_at).seconds
                logging.info(
                    "[%s] Waiting an hour to claim bot, Time left: %s sec",
                    self.pyrogram_client.me.first_name,
                    bot_receive_timeout,
                )
                await asyncio.sleep(bot_receive_timeout)
                robot_data = await self.api.check_robot()

                if robot_data > 0:
                    await self.api.claim_robot()
                    logging.info("[%s] Claimed robot, Value: %s", self.pyrogram_client.me.first_name, robot_data)

            await self.run_clicker()

            full_recharge_time = (
                self.api.last_profile_data.energy_limit // self.api.last_profile_data.recharging_speed - 10
            )

            if self.api.last_profile_data.with_robot:
                full_recharge_time = max(
                    full_recharge_time,
                    60 * 62 - (arrow.now() - self.api.last_clicker_data.last_click_at).seconds,
                )

            logging.info("[%s] Sleeping for %s seconds", self.pyrogram_client.me.first_name, full_recharge_time)

            self.earning_per_loop = (
                self.api.last_profile_data.total_coins - last_total
                if last_total > 0
                else self.api.last_profile_data.total_coins
            )

            await self.log_statistics()
            await asyncio.sleep(full_recharge_time)
