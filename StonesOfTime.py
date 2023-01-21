import concurrent.futures

from Armory import calculate_armory_bonuses
from Enemies import get_enemies_json
from Giants import get_giants_json
from Enemies import get_enemies_json
from Giants import get_giants_json
from Patterns import get_patterns_json
from Upgrades import get_upgrades_json
from Rage import get_rage_json
from Armory import get_armory_info, calculate_armory_bonuses
from Criticals import get_crit_json
from RandomBoxes import get_random_box_json, get_random_box_lower_time, get_random_box_upper_time
from Dimensions import get_dimension_json
from app import *
from operator import itemgetter
import numpy as np
from time import time
from concurrent import futures
from tqdm import tqdm


def get_stones_of_time_json():
    return {
        "Activity": {
            "Coins from enemies": {
                "Per USP": float(26),
                "Decrease": float(0.98),
                "Minimum": float(0.5)
            },
            "Ingame Souls": {
                "Per USP": float(16),
                "Decrease": float(0.4),
                "Minimum": float(1)
            },
            "Bow Souls": {
                "Per USP": float(29),
                "Decrease": float(2.5),
                "Minimum": float(1)
            },
            "Levels": list(range(0, 45))
        },
        "Idle": {
            "Offline Coins": {
                "Per USP": float(41),
                "Decrease": float(2.8),
                "Minimum": float(4)
            },
            "Offline Enemies": {
                "Per USP": float(10),
                "Decrease": float(1.1),
                "Minimum": float(0.9)
            },
            "Critical Souls": {
                "Per USP": float(31),
                "Decrease": float(5.2),
                "Minimum": float(2)
            },
            "Levels": list(range(0, 25))
        },
        "Hope": {
            "Coin Spawn": {
                "Per USP": float(7),
                "Decrease": float(0.2),
                "Minimum": float(0.3)
            },
            "CpS": {
                "Per USP": float(2),
                "Decrease": float(0.1),
                "Minimum": float(1.5)
            },
            "Souls": {
                "Per USP": float(4),
                "Decrease": float(0.07),
                "Minimum": float(2)
            },
            "Levels": list(range(0, 45))
        },
        "Rage": {
            "Rage Souls": {
                "Per USP": float(5),
                "Decrease": float(0.5),
                "Minimum": float(1)
            },
            "Rage Coins": {
                "Per USP": float(16),
                "Decrease": float(0.6),
                "Minimum": float(2)
            },
            "Rage Duration": {
                "Per USP": float(3),
                "Decrease": float(0.1),
                "Minimum": float(1)
            },
            "Levels": list(range(0, 30))
        }
    }


def calculate_bonus(stat, decrease, minimum, USP, current_bonus):
    if USP == 0:
        return current_bonus
    if USP == 1:
        return USP * stat
    else:
        return max(stat - (decrease * (USP - 1)), minimum) + calculate_bonus(stat, decrease, minimum, USP - 1,
                                                                             current_bonus)


def get_stat_multiplier(USP, target_stat):
    stones_of_time_json = get_stones_of_time_json()
    for stone, stats in stones_of_time_json.items():
        if target_stat in stats:
            stat_per_USP = stones_of_time_json[stone][target_stat]["Per USP"]
            decrease_per_USP = stones_of_time_json[stone][target_stat]["Decrease"]
            minimum = stones_of_time_json[stone][target_stat]["Minimum"]
            return calculate_bonus(stat_per_USP, decrease_per_USP, minimum, USP, 0)


def update_bonuses(variables, stone, level):
    Ingame_Souls, Bow_Souls, Critical_Souls, Souls, Rage_Souls = variables
    if stone == "Activity":
        Ingame_Souls *= get_stat_multiplier(level, "Ingame Souls") / 100 + 1
        Bow_Souls *= get_stat_multiplier(level, "Bow Souls") / 100 + 1
    elif stone == "Idle":
        Critical_Souls *= get_stat_multiplier(level, "Critical Souls") / 100 + 1
    elif stone == "Hope":
        Souls *= get_stat_multiplier(level, "Souls") / 100 + 1
    elif stone == "Rage":
        Rage_Souls += get_stat_multiplier(level, "Rage Souls")
    else:
        print("something went wrong with " + stone)
    variables = Ingame_Souls, Bow_Souls, Critical_Souls, Souls, Rage_Souls
    return variables


def calculate_stone_bonuses(USP_allocation):
    Ingame_Souls, Bow_Souls, Critical_Souls, Souls, Rage_Souls = 1, 1, 1, 1, 0
    variables = Ingame_Souls, Bow_Souls, Critical_Souls, Souls, Rage_Souls

    for stone, level in USP_allocation.items():
        variables = update_bonuses(variables, stone, int(level))
    return variables


def get_sot_info():
    stones_of_time_json = get_stones_of_time_json()
    stone_names = []
    stone_levels = {}
    for stone, stat in stones_of_time_json.items():
        stone_names.append(stone)
        stone_levels[stone] = stat["Levels"]
    return stone_names, stone_levels


def calculate_gains(stone_selection):
    dimensions = ["Hills", "Frozen Fields", "Jungle", "Modern City", "Haunted Castle", "Hot Desert", "Mystic Valley",
                  "Factory", "Funky Space"]
    enemy_spawn = ['Need For Kill', 'Enemy Invasion', 'Multa Hostibus', 'Bone Rib Whistle', "Sabrina's Perfume",
                   'Enemy Nests', 'Bring Hell', 'Doomed', 'Reincarnation']
    giant_spawn = ["Zeke's Disgrace", "The Rumbling", "Big Troubles"]
    critical_upgrades = ['Critical Culling', 'Critical Practice', 'Critical Study', 'Critical Training',
                         'Slash The Life', 'Hyper Critical', 'Critical Mushrooms', "That's a lot of damage",
                         'Geode Beetle']
    bow_souls = ['Soul Grabber', 'Augmented Soul Grabber', 'Enhanced Soul Grabber', 'Blessing of Apollo', 'Wind Waker',
                 'Dark Projectiles']
    giant_souls = ["Book of Agony", "Wander's Path"]
    rage_souls = ['Outrage', 'Bad-Tempered', 'Internal Fury']
    enemy_evolutions = ['Hornet', 'Black Hornet', 'Dark Hornet', 'Alpha Worm', 'Beta Worm', 'Gamma Worm', 'Delta Worm',
                        'Red Jelly', 'Blue Jelly', 'Dark Ice Wraith', 'Electric Yeti', 'Venus Carniplant',
                        'Dark Carniplant', 'Poison Mushroom', 'Blue Milk Mushroom', 'Fire Bat', 'Black Demon',
                        'Corrupted Demon', 'Cursed Oak Tree', 'Cursed Willow Tree', 'Blue Wildfire',
                        'Golden Soul Barrel', 'Poisonous Gas', 'Golden Cobra', 'Metal Scorpion']
    giant_evolutions = ["Hills' Giant", "Jade Hills' Giant", 'Adult Yeti', 'Fairy Queen', 'Archdemon', 'Anubis Warrior']
    current_coins = 5e63
    armory_selection = {'Sword': {'Adranos': {'Option': [], 'Level': '14'}},
                        'Armor': {'Kishar': {'Option': ['Enemies'], 'Level': '12'}},
                        'Shield': {'Kishar': {'Option': ['Giant Souls'], 'Level': '14'}},
                        'Ring': {"Victor's Ring": {'Option': ['Critical'], 'Level': '17'}},
                        'Bow': {'Adranos': {'Option': ['Bow Souls'], 'Level': '12'}}}

    Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical_Chance, Electric, Fire, Dark, Enemies = calculate_armory_bonuses(
        armory_selection)
    Ingame_Souls, Bow_Souls_, Critical_Souls_, Souls_, Rage_Souls = calculate_stone_bonuses(stone_selection)
    player_speed = 4
    current_enemies = get_enemy_stats(get_enemies_json(), enemy_evolutions)
    current_giants = get_giant_stats(get_giants_json(), giant_evolutions)
    average_patterns = calculate_average_pattern(current_coins, dimensions)
    pattern_spawn, giant_freq = get_upgrade_stats(enemy_spawn, giant_spawn, Enemies)
    bow_souls_stat, giant_souls_stat, rage_souls_stat = get_soul_stats(bow_souls, giant_souls, rage_souls,
                                                                       Bow_Souls_ * Bow_Souls, Giant_Souls, Rage_Souls)
    critical_chance, critical_souls = get_crit_stats(critical_upgrades)
    Critical_Chance += critical_chance
    Critical_Souls *= critical_souls * Critical_Souls_
    Souls *= Ingame_Souls * Souls_
    variables = Souls, Critical_Souls, Critical_Chance / 100, Electric, Fire, Dark
    base_gains, bow_gains, rage_gains = calculate_average_gains(average_patterns, current_enemies, current_giants,
                                                                pattern_spawn, giant_freq, bow_souls_stat,
                                                                rage_souls_stat, giant_souls_stat, player_speed,
                                                                variables)
    v = list(rage_gains.values())
    d = [s["Souls"] for s in v]
    k = list(rage_gains.keys())
    test = k[d.index(max(d))]
    return stone_selection, max(d), test


def fetch_usp_values(current_usp):
    values = []
    for a in range(10, 40):
        for b in range(12, 25):
            for c in range(10, 45):
                for d in range(10, 20):
                    if a + b + c + d == current_usp:
                        USP_allocation = {
                            "Idle": b,
                            "Activity": a,
                            "Hope": c,
                            "Rage": d
                        }
                        values.append(USP_allocation)
    return values


def optimise(USP):
    USP_values = fetch_usp_values(USP)
    new_values = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        future_to_calc = {executor.submit(calculate_gains, USP_value): USP_value for USP_value in USP_values}
        pbar = tqdm(total=len(future_to_calc))
        for future in concurrent.futures.as_completed(future_to_calc):
            new_values.append(future.result())
            pbar.update(1)
            pbar.refresh()
    # print(new_values)
    max_ = max(new_values, key=itemgetter(2))
    print(max_)


if __name__ == '__main__':
    USP_allocation = {
        "Idle": "17",
        "Activity": "32",
        "Hope": "33",
        "Rage": "19"
    }
    # print(calculate_stone_bonuses(USP_allocation))
    # print(get_sot_info())
    optimise(101)
