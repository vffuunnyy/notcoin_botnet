import enum


class ShopItemType(str, enum.Enum):
    INCREASE_ENERGY_LIMIT = "increaseLimit"
    RESTORATION_ENERGY_SPEED = "speedPerHour"
    MULTIPLE_CLICKS = "multipleClicks"
    ROBOT = "robot"

    CHALLENGE = "challengeCompleted"
    SKIN = "skin"
