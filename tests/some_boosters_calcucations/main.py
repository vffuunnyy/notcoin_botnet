import json
import logging
import math
import sys

from pathlib import Path
from types.arrow import ArrowType

import arrow

from pydantic import BaseModel


# set default arbitrary_types_allowed=True for all pydantic models
pydantic_config = BaseModel.model_config
pydantic_config["arbitrary_types_allowed"] = True

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("launcher.log"),
        logging.StreamHandler(sys.stdout),
    ],
    encoding="utf-8",
)

ROBOT_STARTING_TIMEOUT = 650


# region Boosters


class Booster(BaseModel):
    base_price: int = 100
    level: int = 0
    max_level: int

    base_value: int = 1
    value_per_level: int = 0

    @property
    def price(self) -> int:
        return int(self.base_price * 2**self.level)

    @property
    def possible_to_buy(self) -> bool:
        return self.level < self.max_level

    @property
    def value(self) -> int:
        return self.value_per_level * self.level + self.base_value

    class Config:
        validate_assignment = True


class MultipleClicks(Booster):
    max_level: int = 10000
    base_value: int = 1
    value_per_level: int = 1


class RechargingSpeed(Booster):
    max_level: int = 3
    base_value: int = 1
    value_per_level: int = 1


class EnergyLimit(Booster):
    max_level: int = 10000
    base_value: int = 1000
    value_per_level: int = 500


class Robot(Booster):
    base_price: int = 1000
    max_level: int = 1


# endregion


class SimulationData(BaseModel):
    available_energy: int
    spent_coins: int
    total_coins: int
    balance_coins: int

    multiple_clicks: MultipleClicks
    recharging_speed: RechargingSpeed
    energy_limit: EnergyLimit
    robot: Robot

    start_date: ArrowType = arrow.get("2024.01.01 00:00:00")

    def add_coins(self, coins: int) -> None:
        self.total_coins += coins
        self.balance_coins += coins

    def buy_booster(self, booster: Booster) -> int:
        buy_count = booster.level

        while booster.possible_to_buy and self.balance_coins >= booster.price:
            self.balance_coins -= booster.price
            self.spent_coins += booster.price
            booster.level += 1

        return booster.level - buy_count

    def one_loop_simulation(self, with_robot: bool) -> int:
        """
        :param with_robot: if True, robot will be used

        :return: mining time in seconds
        """
        additional_sleep_time = 0

        boosters = [
            self.energy_limit,
            self.multiple_clicks,
            self.recharging_speed,
        ]

        if with_robot:
            boosters.append(self.robot)

        for booster in boosters:
            additional_sleep_time += 5 * self.buy_booster(booster)

        coins_per_mine = 0

        # if self.robot.level > 0:
        #     coins_per_mine += (sleep_time_between_loops - ROBOT_STARTING_TIMEOUT) * self.recharging_speed.value
        #     additional_sleep_time += 5

        clicks_to_full_mine = math.floor(self.energy_limit.value / self.multiple_clicks.value)
        requests_count = math.ceil(clicks_to_full_mine / 159) + 1
        sleep_between_requests = 10
        recovered_energy = (requests_count - 1) * sleep_between_requests * self.recharging_speed.value

        coins_per_mine += self.multiple_clicks.value * clicks_to_full_mine + recovered_energy
        full_recharge_time = math.floor(self.energy_limit.value / self.recharging_speed.value)

        if self.robot.level > 0:
            coins_per_mine += (full_recharge_time - ROBOT_STARTING_TIMEOUT) * 4
            additional_sleep_time += 5

        self.add_coins(coins_per_mine)

        return (
            requests_count * sleep_between_requests + full_recharge_time + additional_sleep_time
        )  # sleep_time_between_loops

    def one_loop_simulation_basic(self) -> int:
        """

        :return: mining time in seconds
        """
        additional_sleep_time = 0

        boosters = [
            self.robot,
            self.energy_limit,
            self.multiple_clicks,
            self.recharging_speed,
        ]

        for booster in boosters:
            additional_sleep_time += 5 * self.buy_booster(booster)

        sleep_time_between_loops = max(60 * 60, self.energy_limit.value // self.recharging_speed.value)
        coins_per_mine = 0

        if self.robot.level > 0:
            coins_per_mine += (sleep_time_between_loops - ROBOT_STARTING_TIMEOUT) * 4
            additional_sleep_time += 5

        clicks_to_full_mine = math.floor(self.energy_limit.value / self.multiple_clicks.value)
        requests_count = math.ceil(clicks_to_full_mine / 159) + 1
        sleep_between_requests = 10
        coins_per_mine += self.multiple_clicks.value * clicks_to_full_mine

        self.add_coins(coins_per_mine)

        return requests_count * sleep_between_requests + sleep_time_between_loops + additional_sleep_time

    def start_simulation(
        self, limit_days: int, with_robot: bool, basic_strategy: bool = False
    ) -> list[tuple[int, int]]:
        limit_date = self.start_date.shift(days=limit_days)
        balances = []

        logging.info("Start simulation")

        current_day = self.start_date.day
        while self.start_date < limit_date:
            if basic_strategy:
                self.start_date = self.start_date.shift(seconds=self.one_loop_simulation_basic())
            else:
                self.start_date = self.start_date.shift(seconds=self.one_loop_simulation(with_robot))

            if current_day != self.start_date.day:
                current_day = self.start_date.day
                self.add_coins(self.energy_limit.value * 3)
                self.add_coins(self.energy_limit.value * 9 * 3)
                self.start_date = self.start_date.shift(seconds=15 * 6)

            logging.info(
                "Current date: %s | "
                "Total coins: %s | "
                "Energy limit level: %s | ",
                # "Balance coins: %s | "
                # "Spent coins: %s | "
                # "Available energy: %s | "
                # "Multiple clicks level: %s | "
                # "Recharging speed level: %s | "
                # "Robot level: %s",
                self.start_date.format("YYYY.MM.DD HH:mm:ss"),
                self.total_coins,
                self.energy_limit.level,
                # self.balance_coins,
                # self.spent_coins,
                # self.available_energy,
                # self.multiple_clicks.level,
                # self.recharging_speed.level,
                # self.robot.level,
            )

            balances.append((self.start_date.day, self.total_coins))

        logging.info("End simulation")

        return balances


# data = SimulationData(
#     available_energy=0,
#     spent_coins=0,
#     total_coins=0,
#     balance_coins=0,
#     multiple_clicks=MultipleClicks(),
#     recharging_speed=RechargingSpeed(),
#     energy_limit=EnergyLimit(),
#     robot=Robot(),
# )
# balances_with_robot = data.start_simulation(30, True)


results = []
data = SimulationData(
    available_energy=0,
    spent_coins=0,
    total_coins=0,
    balance_coins=0,
    multiple_clicks=MultipleClicks(max_level=3),
    recharging_speed=RechargingSpeed(),
    energy_limit=EnergyLimit(),
    robot=Robot(),
)
balances_basic_strategy = data.start_simulation(30, False, True)


def sum_balances_per_day(data):
    day_balances = {}
    for day, balance in data:
        if day in day_balances:
            day_balances[day] = max(day_balances[day], balance)
        else:
            day_balances[day] = balance
    return day_balances


with_robot_summed = sum_balances_per_day(balances_basic_strategy)
days = sorted(with_robot_summed.keys())
# basic_strategy_summed = [sorted(sum_balances_per_day(r).values()) for r in results]

# Aggregating the summed balances for each day across all strategies
aggregated_balances = {
    "with_robot": [with_robot_summed[day] for day in days],
    # "basic_strategy": [basic_strategy_summed[day] for day in days],
}

with Path("balances.json").open("w", encoding="utf-8") as f:
    json.dump(
        aggregated_balances,
        f,
        indent=4,
    )
