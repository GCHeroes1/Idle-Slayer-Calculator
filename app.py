import copy
import sys

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from Enemies import get_enemies_json
from Giants import get_giants_json
from Patterns import get_patterns_json
from Upgrades import get_upgrades_json
from Rage import get_rage_json
from Armory import get_armory_info, calculate_armory_bonuses
from Criticals import get_crit_json
import numpy as np

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'success': 'ok'})


def get_enemy_helper(enemies):
    evolution_names, evolution_info = [], []
    for key_, value_ in enemies.items():
        if key_ == "Evolutions":
            for key__, value__ in value_.items():
                temp_array = [key__]
                temp_array.extend(list(value__.values()))
                evolution_names.append(key__)
                evolution_info.append(temp_array)
    return evolution_names, evolution_info


def get_enemy_evolutions():
    enemies = get_enemies_json()
    evolution_names, evolution_info = [], []
    for key, value in enemies.items():
        result = list(map(list, zip(*get_enemy_helper(value))))
        if result:
            for res in result:
                evolution_names.append(res[0])
                evolution_info.append(res[1])
    return evolution_names, evolution_info


def get_enemy_stats(evolutions, unlocked_enemies):
    # get a list of the selected evolutions, need to check against the enemies list to find the maximum evolutions
    current_enemies = {}
    for enemy, stats in evolutions.items():
        return_stats = {
            "Dimension": stats["Dimension"],
            "Type": "",
            "Coins": stats["Coins"],
            "Souls": stats["Souls"]
        }
        evolution_names, evolution_info = get_enemy_helper(stats)
        for evolution, evolution_stats in zip(evolution_names, evolution_info):
            if evolution:
                if evolution in unlocked_enemies:
                    return_stats = {
                        "Dimension": stats["Dimension"],
                        "Type": evolution_stats[-4],
                        "Coins": evolution_stats[-3],
                        "Souls": evolution_stats[-2]
                    }
        current_enemies[enemy] = return_stats
    return current_enemies


def calculate_average_pattern(coins):
    patterns_cost = get_upgrades_json()[2]
    patterns = get_patterns_json()
    spawn_level = 0
    for pattern in patterns_cost.values():
        if pattern["Cost"] < coins:
            spawn_level = pattern["Benefit"]

    current_patterns = copy.deepcopy(patterns)
    for dimension, dimension_pattern in patterns.items():
        for enemy, spawn in dimension_pattern.items():
            spawn_ = spawn.copy()
            spawn__ = []
            for pattern in spawn:
                if pattern[1] > spawn_level:
                    spawn_.remove(pattern)
                else:
                    spawn__.append(pattern[0])
            if len(spawn__) == 0:
                spawn__.append(0)
            current_patterns[dimension][enemy] = spawn__

    average_patterns = copy.deepcopy(current_patterns)
    dimension_array = []
    for dimension, dimension_pattern in average_patterns.items():
        totals = []
        total = 0
        for enemy, spawn in dimension_pattern.items():
            totals.append((enemy, sum(spawn)))
            total += len(spawn)
        for enemy, sum_enemies in totals:
            average_patterns[dimension][enemy] = {
                "Average": sum_enemies / total
            }
        dimension_array.append(dimension)
    return average_patterns, dimension_array


def get_giant_evolutions():
    giants = get_giants_json()
    giant_names, giant_info = [], []
    for key, value in giants.items():
        giant_names.append(key)
        giant_info.append([key, value["Coins"], value["Souls"]])
        result = list(map(list, zip(*get_enemy_helper(value))))
        if result:
            for res in result:
                giant_names.append(res[0])
                giant_info.append(res[1])
    giant_info[0].append("7000")  # Hills Giant Cost
    giant_info[2].append("1e8")  # Yeti Giant Cost
    giant_info[3].append(1e35)  # Fairy Giant Cost
    giant_info[4].append(2.5e29)  # Archdemon Giant Cost
    giant_info[5].append("5e18")  # Anubis Giant Cost

    return giant_names, giant_info


def get_giant_stats(evolutions, unlocked_enemies):
    # get a list of the selected giants, need to check against the giants list to see whats unlocked
    current_giants = {}
    for giant, stats in evolutions.items():
        coins, souls = 0, 0
        if giant in unlocked_enemies:
            coins = stats["Coins"]
            souls = stats["Souls"]
        return_stats = {
            "Dimension": stats["Dimension"],
            "Coins": coins,
            "Souls": souls
        }
        evolution_names, evolution_info = get_enemy_helper(stats)
        for evolution, evolution_stats in zip(evolution_names, evolution_info):
            if evolution:
                if evolution in unlocked_enemies:
                    return_stats = {
                        "Dimension": stats["Dimension"],
                        "Coins": evolution_stats[-3],
                        "Souls": evolution_stats[-2]
                    }
        current_giants[giant] = return_stats
    return current_giants


def upgrades_helper(json):
    array = []
    for key, value in json.items():
        array.append([key, value["Cost"], value["Benefit"]])
    return array


def get_upgrade_names():
    bow_upgrade_json, giant_soul_json, _, spawn_upgrade_json, giant_upgrade_json = get_upgrades_json()
    bow_soul_upgrades = upgrades_helper(bow_upgrade_json)
    giant_soul_upgrades = upgrades_helper(giant_soul_json)
    spawn_upgrades = upgrades_helper(spawn_upgrade_json)
    giant_upgrades = upgrades_helper(giant_upgrade_json)
    rage_upgrades = upgrades_helper(get_rage_json())
    return bow_soul_upgrades, giant_soul_upgrades, rage_upgrades, spawn_upgrades, giant_upgrades


def upgrade_stat_helper(upgrades, unlocked_upgrades):
    total = 0
    for upgrade in unlocked_upgrades:
        if upgrade in upgrades:
            total += upgrades[upgrade]["Benefit"]
    return total


def get_upgrade_stats(unlocked_spawn, unlocked_giant):
    # get a list of the selected upgrades, need to check against their lists to see whats unlocked
    _, _, _, spawn_upgrade_json, giant_upgrade_json = get_upgrades_json()
    spawn_stat = upgrade_stat_helper(spawn_upgrade_json, unlocked_spawn)
    giant_stat = upgrade_stat_helper(giant_upgrade_json, unlocked_giant)

    pattern_spawn = (60 / (spawn_stat / 100 + 1) + 90 / (spawn_stat / 100 + 1)) / 2
    giant_spawn = (250 / (giant_stat / 100 + 1) + 450 / (giant_stat / 100 + 1)) / 2
    return pattern_spawn, giant_spawn


def souls_stat_helper(upgrades, unlocked_upgrades):
    total = 1
    for upgrade in unlocked_upgrades:
        if str(upgrade) in upgrades:
            total *= (upgrades[upgrade]["Benefit"] / 100) + 1
    return total


def get_soul_stats(unlocked_bow, unlocked_giant, unlocked_rage):
    bow_upgrade_json, giant_soul_json, _, _, _ = get_upgrades_json()
    rage_souls_json = get_rage_json()
    bow_souls_stat = souls_stat_helper(bow_upgrade_json, unlocked_bow)
    giant_souls_stat = souls_stat_helper(giant_soul_json, unlocked_giant)
    rage_souls_stat = upgrade_stat_helper(rage_souls_json, unlocked_rage)
    if rage_souls_stat != 0:
        rage_souls_stat += 100
    return bow_souls_stat, giant_souls_stat, rage_souls_stat


def get_armory_souls(armory):
    return


def calculate_average_base_gains(average_patterns, current_enemies, current_giants, pattern_spawn, giant_spawn,
                                 giant_bonus, player_speed):
    patterns_per_second = player_speed / pattern_spawn
    giants_per_second = player_speed / giant_spawn

    average_base_gains = {}
    for dimension, dimension_average in average_patterns.items():
        giant_coins, giant_souls = 0, 0
        for key in current_giants.values():
            if dimension == key["Dimension"]:
                giant_coins = key["Coins"] * giants_per_second
                giant_souls = key["Souls"] * giants_per_second * giant_bonus
        coin_reward, soul_reward = 0, 0
        for enemy, spawn in dimension_average.items():
            ## TODO: check if the enemy has a type, and if so, apply the type multiplier to it, take those as parameters
            coin_reward += current_enemies[enemy]["Coins"] * spawn["Average"]
            soul_reward += current_enemies[enemy]["Souls"] * spawn["Average"]
        average_base_gains[dimension] = {
            "Coins": round(coin_reward * patterns_per_second + giant_coins, 2),
            "Souls": round(soul_reward * patterns_per_second + giant_souls, 2)
        }
    return average_base_gains


def calculate_average_bow_gains(average_patterns, current_enemies, current_giants, pattern_spawn, giant_spawn,
                                bow_bonus, player_speed):
    patterns_per_second = player_speed / pattern_spawn
    giants_per_second = player_speed / giant_spawn

    average_bow_gains = {}
    for dimension, dimension_average in average_patterns.items():
        giant_coins, giant_souls = 0, 0
        for key in current_giants.values():
            if dimension == key["Dimension"]:
                giant_coins = key["Coins"] * giants_per_second
                giant_souls = key["Souls"] * giants_per_second
        coin_reward, soul_reward = 0, 0
        for enemy, spawn in dimension_average.items():
            coin_reward += current_enemies[enemy]["Coins"] * spawn["Average"]
            soul_reward += current_enemies[enemy]["Souls"] * spawn["Average"] * bow_bonus
        average_bow_gains[dimension] = {
            "Coins": round(coin_reward * patterns_per_second + giant_coins, 2),
            "Souls": round(soul_reward * patterns_per_second + giant_souls, 2)
        }
    return average_bow_gains


def calculate_average_rage_gains(average_patterns, current_enemies, current_giants, pattern_spawn, giant_spawn,
                                 giant_bonus, rage_bonus, player_speed):
    patterns_per_second = player_speed / pattern_spawn
    giants_per_second = player_speed / giant_spawn

    average_rage_gains = {}
    for dimension, dimension_average in average_patterns.items():
        giant_coins, giant_souls = 0, 0
        for key in current_giants.values():
            if dimension == key["Dimension"]:
                giant_coins = key["Coins"] * giants_per_second
                giant_souls = key["Souls"] * giants_per_second * rage_bonus * giant_bonus
        coin_reward, soul_reward = 0, 0
        for enemy, spawn in dimension_average.items():
            coin_reward += current_enemies[enemy]["Coins"] * spawn["Average"]
            soul_reward += current_enemies[enemy]["Souls"] * spawn["Average"] * rage_bonus
        average_rage_gains[dimension] = {
            "Coins": round(coin_reward * patterns_per_second + giant_coins, 2),
            "Souls": round(soul_reward * patterns_per_second + giant_souls, 2)
        }
    return average_rage_gains


@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/evolutionNames', methods=["GET"])
def evolution_names():
    evolution_names, evolution_info = get_enemy_evolutions()
    return [evolution_names, evolution_info]


@app.route('/dimensions', methods=["GET"])
def dimensions():
    headers = request.headers
    current_coins = float(headers.get("CURRENT_COINS"))
    _, dimension_array = calculate_average_pattern(current_coins)
    return dimension_array


@app.route('/giantNames', methods=["GET"])
def giant_names():
    giant_names, giant_info = get_giant_evolutions()
    return [giant_names, giant_info]


@app.route('/upgradeNames', methods=["GET"])
def upgrade_names():
    bow_soul_upgrades, giant_soul_upgrades, rage_upgrades, spawn_upgrades, giant_upgrades = get_upgrade_names()
    return [bow_soul_upgrades, giant_soul_upgrades, rage_upgrades, spawn_upgrades, giant_upgrades]


@app.route('/armory', methods=["GET"])
def armory():
    armory_json, armory_types, armory_names, armory_options, armory_levels = get_armory_info()
    return [armory_json, armory_types, armory_names, armory_options, armory_levels]


@app.route('/calculateStats', methods=["GET"])
def calculate_stats():
    headers = request.headers
    enemy_spawn = headers.get("ENEMY_SPAWN").split(",")
    giant_spawn = headers.get("GIANT_SPAWN").split(",")
    bow_souls = headers.get("BOW_SOULS").split(",")
    giant_souls = headers.get("GIANT_SOULS").split(",")
    rage_souls = headers.get("RAGE_SOULS").split(",")
    enemy_evolutions = headers.get("ENEMY_EVOLUTIONS").split(",")
    giant_evolutions = headers.get("GIANT_EVOLUTIONS").split(",")
    current_coins = float(headers.get("CURRENT_COINS"))
    armory_selection = eval(headers.get("ARMORY_SELECTION"))
    Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical, Electric, Fire, Dark, Enemies = calculate_armory_bonuses(
        armory_selection)
    player_speed = 4
    current_enemies = get_enemy_stats(get_enemies_json(), enemy_evolutions)
    current_giants = get_giant_stats(get_giants_json(), giant_evolutions)
    average_patterns, __ = calculate_average_pattern(current_coins)
    # bow_soul_upgrades, giant_soul_upgrades, spawn_upgrades, giant_upgrades = get_upgrade_names()
    pattern_spawn, giant_freq = get_upgrade_stats(enemy_spawn, giant_spawn)
    bow_souls_stat, giant_souls_stat, rage_souls_stat = get_soul_stats(bow_souls, giant_souls, rage_souls)
    average_base_gains = calculate_average_base_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
                                                      giant_freq, giant_souls_stat, player_speed)
    average_bow_gains = calculate_average_bow_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
                                                    giant_freq, bow_souls_stat, player_speed)
    average_rage_gains = calculate_average_rage_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
                                                      giant_freq, giant_souls_stat, rage_souls_stat, player_speed)
    return [average_base_gains, average_bow_gains, average_rage_gains]


if __name__ == '__main__':
    # pass
    app.run(host='127.0.0.1', port=5000, debug=True)
    # evolution_names, evolution_info = get_enemy_evolutions()  # done
    # enemy_evolutions = ['Hornet', 'Black Hornet']
    # current_enemies, current_coins = get_enemy_stats(get_enemies_json(), enemy_evolutions)  # done
    # # current_patterns = get_patterns(current_coins)  # done
    # giant_names, giant_info = get_giant_evolutions()  # done
    # giants_unlocked = ["Hills' Giant", 'Adult Yeti', 'Anubis Warrior']
    # current_giants, _ = get_giant_stats(get_giants_json(), giants_unlocked)  # done
    # average_patterns, dimension_array = calculate_average_pattern(current_coins)  # done
    # current_patterns, dimension_array = calculate_average_pattern(0)
    # print(current_patterns)
    # print(dimension_array)

    # enemy_spawn = ["Need For Kill", "Enemy Invasion", "Multa Hostibus", "Bone Rib Whistle", "Sabrina's Perfume",
    #                "Enemy Nests", "Bring Hell", "Doomed", "Reincarnation"]
    # giant_spawn = ["Zeke's Disgrace", "The Rumbling", "Big Troubles"]
    # bow_souls = ["Soul Grabber", "Augmented Soul Grabber", "Enhanced Soul Grabber", "Blessing of Apollo"]
    # giant_souls = ["Book of Agony", "Wander's Path"]
    # enemy_evolutions = ["Hornet", "Black Hornet", "Dark Hornet", "Alpha Worm", "Beta Worm", "Gamma Worm", "Delta Worm",
    #                     "Red Jelly", "Blue Jelly", "Dark Ice Wraith", "Electric Yeti", "Venus Carniplant",
    #                     "Dark Carniplant", "Poison Mushroom", "Blue Milk Mushroom", "Fire Bat", "Black Demon",
    #                     "Corrupted Demon", "Cursed Oak Tree", "Cursed Willow Tree", "Blue Wildfire",
    #                     "Golden Soul Barrel", "Poisonous Gas", "Golden Cobra", "Metal Scorpion"]
    # giant_evolutions = ["Hills' Giant", "Jade Hills' Giant", "Adult Yeti", "Fairy Queen", "Archdemon", "Anubis Warrior"]

    # enemy_spawn = []
    # giant_spawn = []
    # bow_souls = []
    # giant_souls = ["Wander's Path"]
    # enemy_evolutions = []
    # giant_evolutions = ["Anubis Warrior"]
    # current_coins = 0
    # player_speed = 4
    # rage_souls_stat = 100
    # current_enemies, __ = get_enemy_stats(get_enemies_json(), enemy_evolutions)
    # current_giants, __ = get_giant_stats(get_giants_json(), giant_evolutions)
    # average_patterns, __ = calculate_average_pattern(current_coins)
    # # bow_soul_upgrades, giant_soul_upgrades, spawn_upgrades, giant_upgrades = get_upgrade_names()
    # pattern_spawn, giant_freq = get_upgrade_stats(enemy_spawn, giant_spawn)
    # bow_souls_stat, giant_souls_stat = get_soul_stats(bow_souls, giant_souls)
    # average_base_gains = calculate_average_base_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
    #                                                   giant_freq, giant_souls_stat, player_speed)
    # average_bow_gains = calculate_average_bow_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
    #                                                 giant_freq, giant_souls_stat, player_speed)
    # average_rage_gains = calculate_average_rage_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
    #                                                   giant_freq, giant_souls_stat, rage_souls_stat, player_speed)
    # print("test")
