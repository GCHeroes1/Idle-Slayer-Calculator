from Patterns import get_patterns_json
from Enemies import get_enemies_json
from Giants import get_giants_json
from Upgrades import get_upgrades_json
from Conversion import convert_standard_to_exponential
import copy

DIMENSIONS = ["Hills", "Frozen Fields", "Jungle", "Modern City", "Haunted Castle", "Mystic Valley", "Factory",
              "Hot Desert", "Funky Space"]


def set_spawn_level(coins, patterns_cost):
    spawn_level = 0
    for pattern in patterns_cost.values():
        if pattern["Cost"] < coins:
            spawn_level = pattern["Benefit"]
    return spawn_level


def adjust_patterns(spawn_level, patterns):
    to_return = copy.deepcopy(patterns)
    for dimension, dimension_pattern in patterns.items():
        for enemy, spawn in dimension_pattern.items():
            spawn_ = spawn.copy()
            spawn__ = []
            for pattern in spawn:
                if pattern[1] > spawn_level:
                    spawn_.remove(pattern)
                else:
                    spawn__.append(pattern[0])
            to_return[dimension][enemy] = spawn__
    return to_return


def adjust_evolutions(coins, enemies):
    to_return = {}
    for enemy, stats in enemies.items():
        return_stats = {
            "Dimension": stats["Dimension"],
            "Coins": stats["Coins"],
            "Souls": stats["Souls"]
        }
        for evolution, evolution_stats in stats["Evolutions"].items():
            if evolution:
                if evolution_stats["Unlock Cost"] < coins:
                    return_stats = {
                        "Dimension": stats["Dimension"],
                        "Coins": evolution_stats["Coins"],
                        "Souls": evolution_stats["Souls"]
                    }
        to_return[enemy] = return_stats
    return to_return


def calculate_average_pattern(patterns):
    to_return = copy.deepcopy(patterns)
    for dimension, dimension_pattern in to_return.items():
        totals = []
        total = 0
        for enemy, spawn in dimension_pattern.items():
            # spawn_ = spawn.copy()
            totals.append((enemy, sum(spawn)))
            total += len(spawn)
        for enemy, sum_enemies in totals:
            to_return[dimension][enemy] = {
                "Average": sum_enemies / total
            }
    return to_return


def calculate_average_gains(average_patterns, current_enemies, current_giants, patterns_per_second, giants_per_second):
    print("test")
    to_return = {}
    for dimension, dimension_average in average_patterns.items():
        giant_coins, giant_souls = 0, 0
        for key in current_giants.values():
            if dimension == key["Dimension"]:
                giant_coins = key["Coins"] * giants_per_second
                giant_souls = key["Souls"] * giants_per_second
        coin_reward = 0
        soul_reward = 0
        for enemy, spawn in dimension_average.items():
            coin_reward += current_enemies[enemy]["Coins"] * spawn["Average"]
            soul_reward += current_enemies[enemy]["Souls"] * spawn["Average"]
        to_return[dimension] = {
            "Coins": round(coin_reward * patterns_per_second + giant_coins, 2),
            "Souls": round(soul_reward * patterns_per_second + giant_souls, 2)
        }
    return to_return


def calculate_giant_spawn(coins, giants):
    total = 0
    for upgrade, stats in giants.items():
        if stats["Cost"] < coins:
            total += stats["Benefit"]
    return (250 / (total / 100 + 1) + 450 / (total / 100 + 1)) / 2


def calculate_pattern_spawn(coins, enemies):
    total = 0
    for upgrade, stats in enemies.items():
        if stats["Cost"] < coins:
            total += stats["Benefit"]
    return (60 / (total / 100 + 1) + 90 / (total / 100 + 1)) / 2


if __name__ == '__main__':
    patterns_json = get_patterns_json()
    enemies_json = get_enemies_json()
    giants_json = get_giants_json()
    bow_upgrade_json, pattern_upgrade_json, spawn_upgrade_json, giant_upgrade_json = get_upgrades_json()

    COINS = convert_standard_to_exponential("10 Sp")
    PLAYER_SPEED = 4
    SPAWN_LEVEL = set_spawn_level(COINS, pattern_upgrade_json)
    CURRENT_PATTERNS = adjust_patterns(SPAWN_LEVEL, patterns_json)
    CURRENT_ENEMIES = adjust_evolutions(COINS, enemies_json)
    CURRENT_GIANTS = adjust_evolutions(COINS, giants_json)
    AVERAGE_PATTERNS = calculate_average_pattern(CURRENT_PATTERNS)
    GIANT_PER_SECOND = PLAYER_SPEED / calculate_giant_spawn(COINS, giant_upgrade_json)
    PATTERNS_PER_SECOND = PLAYER_SPEED / calculate_pattern_spawn(COINS, spawn_upgrade_json)
    AVERAGE_GAINS_PER_SECOND = calculate_average_gains(AVERAGE_PATTERNS, CURRENT_ENEMIES, CURRENT_GIANTS,
                                                       PATTERNS_PER_SECOND, GIANT_PER_SECOND)
    print("test")
