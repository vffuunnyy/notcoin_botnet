import asyncio
import contextlib
import io
import logging
import random
import sys
import time

from pathlib import Path
from threading import Thread

from pyrogram import Client

from src.models.telegram_settings import TelegramAccountSettings
from src.standard_strategy import StandardStrategy
from src.telegram import auth_session


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("launcher.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
    encoding="utf-8",
)


async def run_client(session_file_name: str) -> None:  # profile_photo_bytes: io.BytesIO) -> None:
    settings = TelegramAccountSettings.model_validate_json(
        Path(f"../sessions_desktop/{session_file_name}.json").read_text(encoding="utf-8")
    )
    session_file = io.BytesIO(Path(f"../sessions_desktop/{session_file_name}.session").read_bytes())
    session = auth_session(session_file, settings)
    app = Client(
        session_file_name,
        api_id=settings.app_id,
        api_hash=settings.app_hash,
        device_model=settings.device,
        system_version=settings.sdk,
        app_version=settings.app_version,
        lang_code=settings.lang_code,
        phone_number=settings.phone,
        password=settings.two_fa,
        lang_pack="tdesktop",
        session_string=session,
        no_updates=False,
    )

    strategy = StandardStrategy("🦉 TestStrategy", app, None)

    await strategy.base_setup()
    await strategy.run_strategy()

    with contextlib.suppress(Exception):
        await app.stop()


if __name__ == "__main__":
    # avatars = cycle([
    #     io.BytesIO(file_path.read_bytes())
    #     for file_path in Path("../avatars/").iterdir()
    #     if file_path.is_file() and file_path.suffix == ".png"
    # ])

    sessions: list[str] = [
        file_path.stem
        for file_path in Path("../sessions_desktop/").iterdir()
        if file_path.is_file() and file_path.suffix == ".json"
    ]
    threads = []

    random.shuffle(sessions)
    for session in sessions:
        thread = Thread(
            target=lambda fp: asyncio.run(run_client(fp)),  # next(avatars))),
            args=(session,),
        )
        thread.start()
        threads.append(thread)
        time.sleep(random.randint(15, 30))  # noqa: S311

    for thread in threads:
        thread.join()
