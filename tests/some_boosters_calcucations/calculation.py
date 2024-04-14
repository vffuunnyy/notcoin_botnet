import pandas as pd


max_energy_levels = range(500, 8500, 500)
energy_recovery_rate = 4
coins_per_click = 4
clicks_per_request = 159
session_duration = 11
energy_per_session = clicks_per_request
coins_per_session = clicks_per_request * coins_per_click
recovery_per_session = 44


def calculate_click_sessions(energy: int) -> int:
    return energy // (energy_per_session - recovery_per_session)


def calculate_bot_coins(energy: int, total_click_time: int, recovery_rate: int, bot_start_time: int) -> int:
    total_time = energy / recovery_rate + total_click_time
    return int(max(total_time - bot_start_time, 0) * 4)


data = {
    "Макс. уровень энергии": max_energy_levels,
    "Время восстановления (сек)": [energy / energy_recovery_rate for energy in max_energy_levels],
    "Циклы кликов": [calculate_click_sessions(energy) for energy in max_energy_levels],
    "Монеты с кликов": [(energy // energy_per_session) * coins_per_session for energy in max_energy_levels],
    "Время кликов (сек)": [(energy // energy_per_session) * session_duration for energy in max_energy_levels],
}
df = pd.DataFrame(data)
df["Монеты с бота"] = [
    calculate_bot_coins(energy, df["Время кликов (сек)"].iloc[i], energy_recovery_rate, 650)
    for i, energy in enumerate(max_energy_levels)
]
df["Общее количество монет"] = df["Монеты с кликов"] + df["Монеты с бота"]

print(df.to_string(index=False))
