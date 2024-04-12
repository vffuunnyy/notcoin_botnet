import base64
import struct
import typing

from stream_sqlite import stream_sqlite


if typing.TYPE_CHECKING:
    import io

    from src.models.telegram_settings import TelegramAccountSettings


def auth_session(
    session_file: "io.BytesIO",
    settings: "TelegramAccountSettings",
) -> str | None:
    auth_key, dc_id = None, None

    for table_name, _, rows in stream_sqlite(session_file, max_buffer_size=1_048_576):
        if table_name == "sessions":
            for row in rows:
                if (
                    all(hasattr(row, attr) for attr in ["auth_key", "dc_id"])
                    and row.auth_key is not None
                    and row.dc_id is not None
                ):
                    auth_key, dc_id = row.auth_key, row.dc_id
                    break

    if None in (auth_key, dc_id):
        return None

    return (
        base64.urlsafe_b64encode(
            struct.pack(
                ">BI?256sQ?",
                dc_id,
                settings.app_id,
                False,
                auth_key,
                999999999,
                False,
            )
        )
        .decode()
        .rstrip("=")
    )
