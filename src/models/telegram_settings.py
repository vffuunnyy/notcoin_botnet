from pydantic import BaseModel, Field


class TelegramAccountSettings(BaseModel):
    session_file: str | None = Field(None, description="Session file")
    phone: str | None = Field(None, description="Phone number")
    register_time: int | None = Field(None, description="Register time")
    app_id: int = Field(..., description="App ID")
    app_hash: str = Field(..., description="App hash")
    sdk: str = Field(..., description="SDK")
    app_version: str = Field(..., description="App version")
    device: str = Field(..., description="Device")
    last_check_time: int | None = Field(None, description="Last check time")
    first_name: str | None = Field(None, description="First name")
    last_name: str | None = Field(None, description="Last name")
    lang_pack: str | None = Field(None, description="Language pack")
    system_lang_pack: str | None = Field(None, description="System language pack")
    lang_code: str | None = Field(None, description="Language code")
    proxy: str | None = Field(None, description="Proxy")
    two_fa: str | None = Field(None, description="Two factor auth")
    ipv6: bool | None = Field(None, description="IPv6")
    username: str | None = Field(None, description="Username")
    avatar: str | None = Field(None, description="Avatar")

    class Config:
        extra = "allow"
