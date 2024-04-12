import asyncio
import json
import logging
import os
import re
import sys
import urllib.parse

from dataclasses import dataclass
from pathlib import Path

import aiohttp

from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.types import DataJSON
from tele_storage import TelethonStorage


directory_files = os.listdir("sessions/")
if len(directory_files) == 0:
    print("No sessions found")
    sys.exit(1)


@dataclass
class SessionData:
    session_file: str
    phone: str
    app_id: int
    app_hash: str
    sdk: str
    app_version: str
    device: str
    system_lang_pack: str
    lang_code: str
    twoFA: str


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("launcher.log"),
        logging.StreamHandler(sys.stdout),
    ],
    encoding="utf-8",
)

for i, file in enumerate(directory_files):
    logging.info(f"{i} - {file}")

    if file.endswith(".json"):
        with open(f"./sessions/{file}", encoding="utf-8") as f:
            session = SessionData(
                **{k: v for k, v in json.load(f).items() if k in SessionData.__annotations__}
            )

url = "https://clicker-api.joincommunity.xyz/auth/webapp-session"
headers = {
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Android WebView";v="120"',
    "DNT": "1",
    "Sec-Ch-Ua-Mobile": "?1",
    "X-Requested-With": "org.telegram.messenger.web",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2007J3SY Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": "https://clicker.joincommunity.xyz/",
    "Sec-Ch-Ua-Platform": '"Android"',
}


async def send_request(data: dict) -> dict | None:
    async with aiohttp.ClientSession() as s, s.post(url, headers=headers, data=json.dumps(data)) as response:
        if response.status == 201:
            result = await response.json()

            if result.get("ok"):
                return result.get("data")
            else:
                print(result)
                return None
        else:
            print("Error:", response.status)
            print(await response.text())
            return None


async def main() -> None:

    app = Client(
        session.session_file,
        api_id=int(session.app_id),
        api_hash=session.app_hash,
        device_model=session.device,
        system_version=session.sdk,
        app_version=session.app_version,
        lang_code=session.lang_code,
        phone_number=session.phone,
        password=session.twoFA,
        lang_pack="tdesktop",
        storage_engine=TelethonStorage(
            name=session.session_file,
            workdir=Path("sessions/"),
            api_id=int(session.app_id),
            test_mode=False,
            is_bot=False,
        ),
    )

    await app.start()

    await app.send_photo("@vffuunnyy", photo="./avatar.jpg", caption="New avatar")
    # logging.info(f"Avatar setting result: {await app.set_profile_photo(photo='./avatar.jpg')}")

    await app.send_message("@notcoin_bot", "/start r_577708_1659140")

    await asyncio.sleep(5)

    while True:
        result = await app.invoke(
            functions.messages.request_web_view.RequestWebView(
                peer=await app.resolve_peer("@notcoin_bot"),
                bot=await app.resolve_peer("@notcoin_bot"),
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
        hash_ = hash_param.group(1) if hash_param else None
        auth_date = auth_date_param.group(1) if auth_date_param else None

        webapp_data = f"query_id={query_id}&user={user}&auth_date={auth_date}&hash={hash_}"

        logging.info(webapp_data)

        with open("webapp_data.txt", "w", encoding="utf-8") as f:
            f.write(webapp_data)

        result = await send_request({"webAppData": webapp_data})
        print(result)

        with open("access_token.txt", "w", encoding="utf-8") as f:
            f.write(result.get("accessToken"))

        await asyncio.sleep(60 * 40)

    await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
