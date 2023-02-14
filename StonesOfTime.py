import concurrent.futures

import json
import csv
from Armory import calculate_armory_bonuses
from RandomBoxes import get_random_box_lower_time, get_random_box_upper_time
from operator import itemgetter
from time import time
from concurrent import futures
from tqdm import tqdm
import requests


def get_stones_of_time_json():
    dict = {
        "Activity": {
            "Coins from enemies": {
                "Per USP": float(26),
                "Decrease": float(0.98),
                "Minimum": float(0.5)
            },
            "in-game Souls": {
                "Per USP": float(16),
                "Decrease": float(0.4),
                "Minimum": float(1)
            },
            "Bow Souls": {
                "Per USP": float(29),
                "Decrease": float(2.5),
                "Minimum": float(1)
            },
            "Levels": list(range(0, 101))
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
            "Levels": list(range(0, 54))
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
            "Levels": list(range(0, 101))
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
            "Levels": list(range(0, 101))
        }
    }
    with open('./data/get_sot_info.json', 'w', encoding='utf8') as fp:
        json.dump(dict, fp, ensure_ascii=False)
    return dict


def get_sot_info():
    stones_of_time_json = get_stones_of_time_json()
    stone_names = []
    stone_levels = {}
    for stone, stat in stones_of_time_json.items():
        stone_names.append(stone)
        stone_levels[stone] = stat["Levels"]
    with open('./data/get_stone_names.csv', 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(stone_names)
        fp.close()
    with open('./data/get_stone_levels.json', 'w', encoding='utf8') as fp:
        json.dump(stone_levels, fp, ensure_ascii=False)
    return stone_names, stone_levels


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
        Ingame_Souls *= get_stat_multiplier(level, "in-game Souls") / 100 + 1
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


endpoint = "https://idle-slayer-calculator.com/"


# endpoint = "http://127.0.0.1:5000/"


def calculate_gains(unlocked_dimensions, unlocked_enemy_spawn_upgrades, unlocked_giant_spawn_upgrades,
                    unlocked_critical_upgrades, unlocked_boost_soul_upgrades, unlocked_bow_soul_upgrades,
                    unlocked_giant_soul_upgrades, unlocked_rage_soul_upgrades, unlocked_enemies, unlocked_giants,
                    unlocked_armory, stone_selection, percentage_rage):
    body_data = {
        "DIMENSIONS": unlocked_dimensions,
        "ENEMY_SPAWN": unlocked_enemy_spawn_upgrades,
        "GIANT_SPAWN": unlocked_giant_spawn_upgrades,
        "CRITICAL_UPGRADES": unlocked_critical_upgrades,
        "BOOST_SOULS": unlocked_boost_soul_upgrades,
        "BOW_SOULS": unlocked_bow_soul_upgrades,
        "GIANT_SOULS": unlocked_giant_soul_upgrades,
        "RAGE_SOULS": unlocked_rage_soul_upgrades,
        "ENEMY_EVOLUTIONS": unlocked_enemies,
        "GIANT_EVOLUTIONS": unlocked_giants,
        "ARMORY_SELECTION": str(unlocked_armory),
        "STONE_SELECTION": str(stone_selection)
    }
    url = endpoint + "calculateStats"
    r = requests.post(url=url, json=body_data)

    base_gains, bow_gains, rage_gains, bow_souls_stat, rage_souls_stat = eval(r.text)

    rage_duration = 1
    if "Rage" in stone_selection:
        rage_duration = 0.5 * get_stat_multiplier(int(stone_selection["Rage"]), "Rage Duration") / 100 + 1

    percentage_bow = 1 - percentage_rage
    best_souls = 0
    best_dimension = ""
    average_gains = {}
    for dimension, values in base_gains.items():
        # print(bow_gains[dimension]["Souls"], rage_gains[dimension]["Souls"])
        average_gains[dimension] = percentage_bow * bow_gains[dimension]["Souls"]
        average_gains[dimension] += percentage_rage * rage_gains[dimension]["Souls"] * rage_duration
        if average_gains[dimension] > best_souls:
            best_souls = average_gains[dimension]
            best_dimension = dimension
    # bow_reward_values = list(bow_gains.values())
    # bow_soul_values = [soul["Souls"] for soul in bow_reward_values]
    # bow_soul_keys = list(rage_gains.keys())
    # bow_best_dimension = bow_soul_keys[bow_soul_values.index(max(bow_soul_values))]
    #
    # rage_reward_values = list(rage_gains.values())
    # rage_soul_values = [soul["Souls"] for soul in rage_reward_values]
    # rage_soul_keys = list(rage_gains.keys())
    # rage_best_dimension = rage_soul_keys[rage_soul_values.index(max(rage_soul_values))]
    return best_souls, best_dimension, stone_selection


def process_usp(value):
    bound = 20
    if value - bound < 0:
        return 0, value + bound
    return value - bound, value + bound


def fetch_usp_values(current_usp_allocation):
    # current_usp_allocation = {
    #     "Idle": "3",
    #     "Activity": "32",
    #     "Hope": "33",
    #     "Rage": "19"
    # }
    current_usp = 0
    idle_min, idle_max, active_min, active_max, hope_min, hope_max, rage_min, rage_max = 0, 0, 0, 0, 0, 0, 0, 0
    if "Idle" in current_usp_allocation:
        current_usp += int(current_usp_allocation["Idle"])
        # idle_min, idle_max = int(current_usp_allocation["Idle"]), int(current_usp_allocation["Idle"])
        idle_min, idle_max = process_usp(int(current_usp_allocation["Idle"]))
    if "Activity" in current_usp_allocation:
        current_usp += int(current_usp_allocation["Activity"])
        active_min, active_max = process_usp(int(current_usp_allocation["Activity"]))
    if "Hope" in current_usp_allocation:
        current_usp += int(current_usp_allocation["Hope"])
        hope_min, hope_max = process_usp(int(current_usp_allocation["Hope"]))
    if "Rage" in current_usp_allocation:
        current_usp += int(current_usp_allocation["Rage"])
        # rage_min, rage_max = int(current_usp_allocation["Rage"]), int(current_usp_allocation["Rage"])
        rage_min, rage_max = process_usp(int(current_usp_allocation["Rage"]))
    values = []
    step = 2
    for active in range(active_min, active_max + 1, step):
        for idle in range(idle_min, idle_max + 1, step):
            for hope in range(hope_min, hope_max + 1, step):
                for rage in range(rage_min, rage_max + 1, step):
                    if active + idle + hope + rage == current_usp:
                        USP_allocation = {
                            "Idle": idle,
                            "Activity": active,
                            "Hope": hope,
                            "Rage": rage
                        }
                        values.append(USP_allocation)
    return values


def optimise(unlocked_dimensions, unlocked_enemy_spawn_upgrades, unlocked_giant_spawn_upgrades,
             unlocked_critical_upgrades, unlocked_boost_soul_upgrades, unlocked_bow_soul_upgrades,
             unlocked_giant_soul_upgrades, unlocked_rage_soul_upgrades, unlocked_enemies,
             unlocked_giants, unlocked_armory, USP_allocation, percentage_rage):
    USP_values = fetch_usp_values(USP_allocation)
    new_values = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        future_to_calc = {executor.submit(calculate_gains, unlocked_dimensions, unlocked_enemy_spawn_upgrades,
                                          unlocked_giant_spawn_upgrades,
                                          unlocked_critical_upgrades, unlocked_boost_soul_upgrades,
                                          unlocked_bow_soul_upgrades,
                                          unlocked_giant_soul_upgrades, unlocked_rage_soul_upgrades, unlocked_enemies,
                                          unlocked_giants, unlocked_armory, USP_value, percentage_rage): USP_value for
                          USP_value in USP_values}
        pbar = tqdm(total=len(future_to_calc))
        for future in concurrent.futures.as_completed(future_to_calc):
            new_values.append(future.result())
            pbar.update(1)
            pbar.refresh()
    # print(new_values)
    max_ = max(new_values, key=itemgetter(0))
    print(max_)


if __name__ == '__main__':
    dict = get_stones_of_time_json()
    stone_names, stone_levels = get_sot_info()
    USP_allocation = {
        "Idle": "17",
        "Activity": "32",
        "Hope": "33",
        "Rage": "19"
    }
    # USP_allocation = {'Idle': '17', 'Activity': '32', 'Hope': '33', 'Rage': '19'}
    # USP_allocation = {'Idle': 6, 'Activity': 30, 'Hope': 31, 'Rage': 34}
    unlocked_dimensions = ["Hills", "Frozen Fields", "Jungle", "Modern City", "Haunted Castle", "Hot Desert",
                           "Mystic Valley", "Factory", "Funky Space"]
    unlocked_enemy_spawn_upgrades = ['Need For Kill', 'Enemy Invasion', 'Multa Hostibus', 'Bone Rib Whistle',
                                     "Sabrina's Perfume",
                                     'Enemy Nests', 'Bring Hell', 'Doomed', 'Reincarnation']
    unlocked_giant_spawn_upgrades = ["Zeke's Disgrace", "The Rumbling", "Big Troubles"]
    unlocked_critical_upgrades = ['Critical Culling', 'Critical Practice', 'Critical Study', 'Critical Training',
                                  'Slash The Life', 'Hyper Critical', 'Critical Mushrooms', "That's a lot of damage",
                                  'Geode Beetle']
    unlocked_boost_soul_upgrades = ["Boost Kill"]
    unlocked_bow_soul_upgrades = ['Soul Grabber', 'Augmented Soul Grabber', 'Enhanced Soul Grabber',
                                  'Blessing of Apollo', 'Wind Waker', 'Dark Projectiles']
    unlocked_giant_soul_upgrades = ["Book of Agony", "Wander's Path"]
    unlocked_rage_soul_upgrades = ['Outrage', 'Bad-Tempered', 'Internal Fury']
    unlocked_enemies = ['Hornet', 'Black Hornet', 'Dark Hornet', 'Alpha Worm', 'Beta Worm', 'Gamma Worm', 'Delta Worm',
                        'Red Jelly', 'Blue Jelly', 'Dark Ice Wraith', 'Electric Yeti', 'Venus Carniplant',
                        'Dark Carniplant', 'Poison Mushroom', 'Blue Milk Mushroom', 'Fire Bat', 'Black Demon',
                        'Corrupted Demon', 'Cursed Oak Tree', 'Cursed Willow Tree', 'Blue Wildfire',
                        'Golden Soul Barrel', 'Poisonous Gas', 'Golden Cobra', 'Metal Scorpion']
    unlocked_giants = ["Hills' Giant", "Jade Hills' Giant", 'Adult Yeti', 'Fairy Queen', 'Archdemon', 'Anubis Warrior']
    unlocked_armory = {'Sword': {'Adranos': {'Option': [], 'Level': '14'}},
                       'Armor': {'Kishar': {'Option': ['Enemies'], 'Level': '12'}},
                       'Shield': {'Kishar': {'Option': ['Giant Souls'], 'Level': '14'}},
                       'Ring': {"Victor's Ring": {'Option': ['Critical'], 'Level': '17'}}}
    # 'Bow': {'Adranos': {'Option': ['Bow Souls'], 'Level': '12'}}}

    # print(fetch_usp_values(current_usp_allocation=USP_allocation))
    print(calculate_gains(unlocked_dimensions, unlocked_enemy_spawn_upgrades, unlocked_giant_spawn_upgrades,
                          unlocked_critical_upgrades, unlocked_boost_soul_upgrades, unlocked_bow_soul_upgrades,
                          unlocked_giant_soul_upgrades, unlocked_rage_soul_upgrades, unlocked_enemies,
                          unlocked_giants, unlocked_armory, USP_allocation, percentage_rage=0.1))

    optimise(unlocked_dimensions, unlocked_enemy_spawn_upgrades, unlocked_giant_spawn_upgrades,
             unlocked_critical_upgrades, unlocked_boost_soul_upgrades, unlocked_bow_soul_upgrades,
             unlocked_giant_soul_upgrades, unlocked_rage_soul_upgrades, unlocked_enemies,
             unlocked_giants, unlocked_armory, USP_allocation, percentage_rage=1)

    print("test")
    # print(calculate_stone_bonuses(USP_allocation))
    # print(get_sot_info())
    # optimise(101)
    # print(calculate_stats())
