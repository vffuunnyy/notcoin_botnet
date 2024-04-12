from pydantic import BaseModel


class Booster(BaseModel):
    price: int
    level: int = 0
    max_level: int

    @property
    def possible_to_buy(self) -> bool:
        return self.level < self.max_level


class MultipleClicks(Booster):
    max_level: int = 3


class RechargingSpeed(Booster):
    max_level: int = 3


class EnergyLimit(Booster):
    max_level: int = 10000


class Robot(Booster):
    max_level: int = 1
