from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from src.custom_types import ArrowType
from src.enums import ShopItemType


BaseModel.model_config["arbitrary_types_allowed"] = True
BaseModel.model_config["extra"] = "allow"


class BaseResponse(BaseModel):
    ok: bool
    data: list | dict | int


class ExceptionData(BaseModel):
    message: str
    error: str
    status_code: int = Field(..., alias="statusCode")


class BaseClickerData(BaseModel):
    id: int = Field(..., description="Internal clicker ID")
    user_id: int = Field(..., alias="userId", description="Internal user ID")
    team_id: int | None = Field(None, alias="teamId", description="Internal team ID")
    league_id: int = Field(0, alias="leagueId", description="Internal league ID")
    avatar: str | None = Field(None, description="Avatar")

    total_coins: int = Field(0, alias="totalCoins", description="Total coins")
    spent_coins: int = Field(0, alias="spentCoins", description="Spent coins")
    auto_clicks: int = Field(0, alias="autoClicks", description="Auto clicks")

    balance: int = Field(0, alias="balanceCoins", description="Balance coins")
    energy_limit: int = Field(0, alias="limitCoins", description="Limit coins")
    recharging_speed: int = Field(0, alias="miningPerTime", description="Mining per time")
    multiple_clicks: int = Field(0, alias="multipleClicks", description="Multiple clicks")
    with_robot: bool = Field(False, alias="withRobot", description="With robot")

    turbo_times: int = Field(0, alias="turboTimes", description="Turbo times")

    created_at: ArrowType | None = Field(None, alias="createdAt", description="Created at")
    last_click_at: ArrowType | None = Field(None, alias="lastMiningAt", description="Last mining at")

    last_available_energy: int = Field(0, alias="lastAvailableCoins", description="Last available coins")
    available_energy: int = Field(0, alias="availableCoins", description="Available coins")


class TaskData(BaseModel):
    id: int = Field(..., description="Internal clicker ID")
    name: str = Field(..., description="Name")
    type: str = Field(..., description="Type")
    coins: int = Field(..., description="Coins")
    max_count: int = Field(..., alias="max", description="Max count")
    link: str | None = Field(None, description="Link")
    image: str | None = Field(None, description="Image URL")
    status: str = Field(..., description="Status")
    is_daily: bool = Field(..., alias="isDaily", description="Is daily")
    entity_id: int | None = Field(None, alias="entityId", description="Entity ID")
    created_at: ArrowType = Field(..., alias="createdAt", description="Created at")


class CompletedTaskData(BaseModel):
    id: int = Field(..., description="Internal clicker ID")
    task_id: int = Field(..., alias="taskId", description="Task ID")
    user_id: int = Field(..., alias="userId", description="User ID")
    created_at: ArrowType = Field(..., alias="createdAt", description="Created at")
    task: TaskData = Field(..., description="Task")


class SquadData(BaseModel):
    id: int = Field(..., description="Internal squad ID")
    name: str | None = Field(None, description="Squad name")
    slug: str | None = Field(None, description="Squad slug")
    chat_id: int | None = Field(None, alias="chatId", description="Squad chat ID")
    league_id: int = Field(0, alias="leagueId", description="Internal league ID")
    logo: str | None = Field(None, description="Squad logo")

    coins: int = Field(0, description="Squad coins")
    count: int | None = Field(None, description="Squad members count")

    created_at: ArrowType = Field(..., alias="createdAt", description="Created at")


class UserData(BaseModel):
    id: int = Field(..., description="Internal user ID")
    telegram_id: int = Field(..., alias="telegramId", description="Telegram user ID")
    username: str | None = Field(None, description="Telegram username")
    first_name: str | None = Field(None, alias="firstName", description="Telegram first name")
    last_name: str | None = Field(None, alias="lastName", description="Telegram last name")
    locale: str = Field(None, description="Telegram locale")
    friendly_address: str | None = Field(None, alias="friendlyAddress", description="Friendly address")
    is_premium: bool = Field(False, alias="isPremium")
    is_blocked: bool = Field(False, alias="isBlocked")
    is_force_blocked: bool = Field(False, alias="isForceBlocked")
    role: str | None = Field(None, description="User role")
    payload: str | None = Field(None, description="User payload (Unknown)")
    last_notified_at: ArrowType = Field(None, alias="lastNotifiedAt", description="Last notified at")
    created_at: ArrowType = Field(..., alias="createdAt", description="Created at")
    touched_after_notification: bool = Field(
        False, alias="touchedAfterNotification", description="Touched after notification"
    )
    deleted_at: ArrowType = Field(None, alias="deletedAt", description="Deleted at")


class ShopItemData(BaseModel):
    id: int = Field(..., description="Internal clicker ID")
    name: str = Field(..., description="Name")
    description: str | None = Field(None, description="Description")
    type: ShopItemType = Field(..., description="Type")
    image: str | None = Field(None, description="Image URL")
    value: int | None = Field(None, alias="coins", description="Coins")
    price: int | None = Field(None, description="Price")
    max_level: int | None = Field(None, alias="max", description="Max level")
    coefficient: int | None = Field(None, description="Coefficient")
    is_partner: bool | None = Field(None, alias="isPartner", description="Is partner")
    is_task: bool | None = Field(None, alias="isTask", description="Is task")
    is_featured: bool | None = Field(None, alias="isFeatured", description="Is featured")
    status: str | None = Field(None, description="Status")
    locale: str | None = Field(None, description="Locale")
    excepted_locale: str | None = Field(None, alias="exceptedLocale", description="Excepted locale")
    category: str | None = Field(None, description="Category")
    min_league_id: int | None = Field(None, alias="minLeagueId", description="Min league ID")
    challenge_id: int | None = Field(None, alias="challengeId", description="Challenge ID")
    live_time_in_seconds: int | None = Field(None, alias="liveTimeInSeconds", description="Live time in seconds")
    created_at: ArrowType = Field(None, alias="createdAt", description="Created at")
    is_completed: bool | None = Field(None, alias="isCompleted", description="Is completed")
    count: int | None = Field(0, description="Count")


class BoostXProfile(BaseModel):
    id: int = Field(..., description="Internal clicker ID")
    profile_id: int = Field(..., alias="profileId", description="Profile ID")
    boost_id: int = Field(..., alias="boostId", description="Boost ID")
    value: int = Field(..., description="Value")
    status: str = Field(..., description="Status")
    expires_at: ArrowType = Field(None, alias="expiresAt", description="Expires at")
    is_applied: bool = Field(..., alias="isApplied", description="Is applied")
    is_expired: bool = Field(..., alias="isExpired", description="Is expired")
    created_at: ArrowType = Field(..., alias="createdAt", description="Created at")
    clicker_boost: ShopItemData = Field(..., alias="clickerBoost", description="Clicker boost")


class ProfileData(BaseClickerData):
    user: UserData = Field(..., description="User data")
    squad: SquadData | None = Field(None, alias="clickerTeam", description="Clicker team")
    clicker_boost_x_profile: list[BoostXProfile] | None = Field(
        None, alias="clickerBoostXProfile", description="Clicker boost X profile"
    )


class ClickData(BaseClickerData):
    hash: list[str] = Field(..., description="Hash")


class WebAppSessionData(BaseModel):
    user_id: int = Field(..., alias="userId", description="User ID")
    access_token: str = Field(..., alias="accessToken", description="Access token")
    refresh_token: str = Field(..., alias="refreshToken", description="Refresh token")


class CheckTurboData(BaseModel):
    turbo: Annotated[bool, BeforeValidator(lambda x: bool(x))] = Field(..., description="Turbo")


class ActiveTurboData(BaseModel):
    multiple: int = Field(..., description="Multiple")
    expire: int = Field(..., description="Expire")
