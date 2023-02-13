import copy

import flask
import json
import csv
from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
from flask_api import status
from flask_cors import CORS, cross_origin
from Armory import calculate_armory_bonuses
from StonesOfTime import calculate_stone_bonuses
from RandomBoxes import get_random_box_lower_time, get_random_box_upper_time, get_box_probabilities

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app, support_credentials=True)


@app.route("/login")
@cross_origin(supports_credentials=True)
def login():
    return jsonify({'success': 'ok'})


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_enemy_helper(enemies):
    # for evolution, evolution_info in enemies["Evolutions"]:

    evolution_info = []
    for key_, value_ in enemies.items():
        if key_ == "Evolutions":
            for key__, value__ in value_.items():
                temp_array = [key__]
                temp_array.extend(list(value__.values()))
                evolution_info.append(temp_array)
    return evolution_info


def get_enemy_evolutions():
    with open('./data/get_enemies.json', 'r') as fp:
        enemies = json.loads(fp.read())
    evolution_info = []
    for key, value in enemies.items():
        result = get_enemy_helper(value)
        if result:
            for res in result:
                evolution_info.append(res)
    return evolution_info


def get_enemy_stats(current_coins, evolutions, unlocked_enemies):
    # get a list of the selected evolutions, need to check against the enemies list to find the maximum evolutions
    current_enemies = {}
    for enemy, stats in evolutions.items():
        return_stats = {
            "Dimension": stats["Dimension"],
            "Type": "",
            "Coins": stats["Coins"],
            "Souls": stats["Souls"]
        }
        for evolution, evolution_stats in stats["Evolutions"].items():
            if evolution:
                if evolution in unlocked_enemies:
                    return_stats = {
                        "Dimension": stats["Dimension"],
                        "Type": evolution_stats["Type"],
                        "Coins": evolution_stats["Coins"],
                        "Souls": evolution_stats["Souls"]
                    }
                    if isfloat(evolution_stats["Cost"]):
                        if current_coins < evolution_stats["Cost"]:
                            current_coins = evolution_stats["Cost"]
        current_enemies[enemy] = return_stats
    return current_enemies, current_coins


def calculate_average_pattern(coins, unlocked_dimensions):
    with open('./data/get_dimension_patterns.json', 'r') as fp:
        patterns = json.loads(fp.read())
    with open('./data/get_patterns_cost.json', 'r') as fp:
        patterns_cost = json.loads(fp.read())
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

    average_patterns = {}
    for dimension in unlocked_dimensions:
        average_patterns[dimension] = {}
        totals = []
        total = 0
        for enemy, spawn in current_patterns[dimension].items():
            totals.append((enemy, sum(spawn)))
            total += len(spawn)
        for enemy, sum_enemies in totals:
            average_patterns[dimension][enemy] = {
                "Average": sum_enemies / total
            }
    return average_patterns


def get_giant_evolutions():
    with open('./data/get_giants.json', 'r') as fp:
        giants = json.loads(fp.read())
    giant_info = []
    for key, value in giants.items():
        giant_info.append([key, value["Coins"], value["Souls"], value["Cost"], value["Standard Cost"]])
        result = get_enemy_helper(value)
        if result:
            for res in result:
                giant_info.append(res)
    return giant_info


def get_giant_stats(current_coins, evolutions, unlocked_enemies):
    # get a list of the selected giants, need to check against the giants list to see whats unlocked
    current_giants = {}
    for giant, stats in evolutions.items():
        coins, souls = 0, 0
        if giant in unlocked_enemies:
            coins = stats["Coins"]
            souls = stats["Souls"]
            if isfloat(evolutions[giant]["Cost"]):
                if current_coins < float(evolutions[giant]["Cost"]):
                    current_coins = float(evolutions[giant]["Cost"])
        return_stats = {
            "Dimension": stats["Dimension"],
            "Coins": coins,
            "Souls": souls
        }
        for evolution, evolution_stats in stats["Evolutions"].items():
            if evolution:
                if evolution in unlocked_enemies:
                    return_stats = {
                        "Dimension": stats["Dimension"],
                        "Coins": evolution_stats["Coins"],
                        "Souls": evolution_stats["Souls"]
                    }
                    if isfloat(evolution_stats["Cost"]):
                        if current_coins < float(evolution_stats["Cost"]):
                            current_coins = float(evolution_stats["Cost"])
        current_giants[giant] = return_stats
    return current_giants, current_coins


def upgrades_helper(json):
    array = []
    for key, value in json.items():
        array.append([key, value["Cost"], value["Standard Cost"]])
    return array


def get_upgrade_names():
    with open('./data/get_boost_souls.json', 'r') as fp:
        boost_soul_json = json.loads(fp.read())
    with open('./data/get_bow_souls.json', 'r') as fp:
        bow_soul_json = json.loads(fp.read())
    with open('./data/get_giant_souls.json', 'r') as fp:
        giant_soul_json = json.loads(fp.read())
    with open('./data/get_enemy_spawn.json', 'r') as fp:
        enemy_spawn_json = json.loads(fp.read())
    with open('./data/get_giant_spawn.json', 'r') as fp:
        giant_spawn_json = json.loads(fp.read())
    with open('./data/get_rage_souls.json', 'r') as fp:
        rage_soul_json = json.loads(fp.read())
    with open('./data/get_crit.json', 'r') as fp:
        crit_json = json.loads(fp.read())
    with open('./data/get_random_box.json', 'r') as fp:
        random_box_json = json.loads(fp.read())
    with open('./data/get_random_box_extra_options.json', 'r') as fp:
        random_box_extra_options_json = json.loads(fp.read())
    with open('./data/get_dimension.json', 'r') as fp:
        dimension_json = json.loads(fp.read())
    boost_soul_upgrades = upgrades_helper(boost_soul_json)
    bow_soul_upgrades = upgrades_helper(bow_soul_json)
    giant_soul_upgrades = upgrades_helper(giant_soul_json)
    spawn_upgrades = upgrades_helper(enemy_spawn_json)
    giant_upgrades = upgrades_helper(giant_spawn_json)
    rage_upgrades = upgrades_helper(rage_soul_json)
    critical_upgrades = upgrades_helper(crit_json)
    random_box_upgrades = upgrades_helper(random_box_json)
    random_box_options = upgrades_helper(random_box_extra_options_json)
    dimension_unlocks = upgrades_helper(dimension_json)
    return boost_soul_upgrades, bow_soul_upgrades, giant_soul_upgrades, rage_upgrades, spawn_upgrades, giant_upgrades, \
           critical_upgrades, random_box_upgrades, dimension_unlocks, random_box_options


def upgrade_stat_helper(current_coins, upgrades, unlocked_upgrades):
    total = 0
    for upgrade in unlocked_upgrades:
        if upgrade in upgrades:
            total += upgrades[upgrade]["Benefit"]
            if isfloat(upgrades[upgrade]["Cost"]):
                if current_coins < float(upgrades[upgrade]["Cost"]):
                    current_coins = float(upgrades[upgrade]["Cost"])
    return float(total), current_coins


def get_upgrade_stats(current_coins, unlocked_spawn, unlocked_giant, Enemies):
    # get a list of the selected upgrades, need to check against their lists to see whats unlocked
    with open('./data/get_enemy_spawn.json', 'r') as fp:
        enemy_spawn_json = json.loads(fp.read())
    with open('./data/get_giant_spawn.json', 'r') as fp:
        giant_spawn_json = json.loads(fp.read())
    spawn_stat, current_coins = upgrade_stat_helper(current_coins, enemy_spawn_json, unlocked_spawn)
    giant_stat, current_coins = upgrade_stat_helper(current_coins, giant_spawn_json, unlocked_giant)
    spawn_stat += Enemies
    pattern_spawn = (60 / (spawn_stat / 100 + 1) + 90 / (spawn_stat / 100 + 1)) / 2
    giant_spawn = (250 / (giant_stat / 100 + 1) + 450 / (giant_stat / 100 + 1)) / 2
    return pattern_spawn, giant_spawn, current_coins


def souls_stat_helper(current_coins, upgrades, unlocked_upgrades):
    total = 1
    for upgrade in unlocked_upgrades:
        if str(upgrade) in upgrades:
            total *= (upgrades[upgrade]["Benefit"] / 100) + 1
            if isfloat(upgrades[upgrade]["Cost"]):
                if current_coins < float(upgrades[upgrade]["Cost"]):
                    current_coins = float(upgrades[upgrade]["Cost"])
    return total, current_coins


def get_soul_stats(current_coins, unlocked_boost, unlocked_bow, unlocked_giant, unlocked_rage):
    with open('./data/get_boost_souls.json', 'r') as fp:
        boost_soul_json = json.loads(fp.read())
    with open('./data/get_bow_souls.json', 'r') as fp:
        bow_soul_json = json.loads(fp.read())
    with open('./data/get_giant_souls.json', 'r') as fp:
        giant_soul_json = json.loads(fp.read())
    with open('./data/get_rage_souls.json', 'r') as fp:
        rage_soul_json = json.loads(fp.read())
    boost_souls_stat, current_coins = souls_stat_helper(current_coins, boost_soul_json, unlocked_boost)
    bow_souls_stat, current_coins = souls_stat_helper(current_coins, bow_soul_json, unlocked_bow)
    giant_souls_stat, current_coins = souls_stat_helper(current_coins, giant_soul_json, unlocked_giant)
    rage_souls_stat, current_coins = upgrade_stat_helper(current_coins, rage_soul_json, unlocked_rage)
    if rage_souls_stat != 0:
        rage_souls_stat += 100
    return boost_souls_stat, bow_souls_stat, giant_souls_stat, rage_souls_stat, current_coins


def crit_helper(current_coins, upgrades, unlocked_upgrades):
    crit_chance = 0
    crit_multiplier = 1
    for upgrade in unlocked_upgrades:
        if str(upgrade) in upgrades:
            if "Critical" in upgrades[upgrade]:
                crit_chance += upgrades[upgrade]["Critical"]
            if "Critical Souls" in upgrades[upgrade]:
                crit_multiplier *= (upgrades[upgrade]["Critical Souls"] / 100) + 1
            if isfloat(upgrades[upgrade]["Cost"]):
                if current_coins < float(upgrades[upgrade]["Cost"]):
                    current_coins = float(upgrades[upgrade]["Cost"])
    return crit_chance, crit_multiplier, current_coins


def get_crit_stats(current_coins, critical_upgrades):
    with open('./data/get_crit.json', 'r') as fp:
        crit_json = json.loads(fp.read())
    critical_chance, critical_multiplier, current_coins = crit_helper(current_coins, crit_json, critical_upgrades)
    return critical_chance, critical_multiplier, current_coins


def calc_type_multiplier(Electric, Fire, Dark, enemy_type):
    multiplier = 1
    if enemy_type == "Electric":
        return multiplier * Electric
    elif enemy_type == "Fire":
        return multiplier * Fire
    elif enemy_type == "Dark":
        return multiplier * Dark
    else:
        return multiplier


def calculate_average_gains(average_patterns, current_enemies, current_giants, pattern_spawn, giant_spawn, boost_bonus,
                            bow_bonus, rage_bonus, giant_bonus, player_speed, variables, bow=False, rage=False):
    Souls, Critical_Souls, Critical_Chance, Electric, Fire, Dark = variables
    patterns_per_second = player_speed / pattern_spawn
    giants_per_second = player_speed / giant_spawn
    if bow_bonus != 1: bow = True
    if rage_bonus != 0: rage = True
    average_base_gains = {}
    average_bow_gains = {}
    average_rage_gains = {}

    for dimension, dimension_average in average_patterns.items():
        average_bow_gains[dimension] = {
            "Coins": round(0, 2),
            "Souls": round(0, 2)
        }
        average_rage_gains[dimension] = {
            "Coins": round(0, 2),
            "Souls": round(0, 2)
        }
        giant_coin_reward, giant_soul_reward = 0, 0
        for key in current_giants.values():
            if dimension == key["Dimension"]:
                giant_souls = key["Souls"] * giants_per_second * giant_bonus * Souls
                giant_souls_crit = (giant_souls * (1 - Critical_Chance)) + (
                        giant_souls * Critical_Chance * Critical_Souls)

                giant_coin_reward = key["Coins"] * giants_per_second
                giant_soul_reward = giant_souls_crit
        enemy_coin_reward, enemy_soul_reward = 0, 0
        for enemy, spawn in dimension_average.items():
            enemy_type = current_enemies[enemy]["Type"]
            type_multiplier = calc_type_multiplier(Electric, Fire, Dark, enemy_type)
            enemy_souls_multiplier = Souls * type_multiplier
            enemy_souls = current_enemies[enemy]["Souls"] * spawn["Average"] * enemy_souls_multiplier
            enemy_souls_crit = (enemy_souls * (1 - Critical_Chance)) + (enemy_souls * Critical_Chance * Critical_Souls)

            enemy_coin_reward += current_enemies[enemy]["Coins"] * spawn["Average"] * patterns_per_second
            enemy_soul_reward += enemy_souls_crit * patterns_per_second
        average_base_gains[dimension] = {
            "Coins": round(enemy_coin_reward + giant_coin_reward, 2),
            "Souls": round((enemy_soul_reward + giant_soul_reward) * boost_bonus, 2)
        }
        if bow:
            enemy_reward_bow = enemy_soul_reward * bow_bonus
            average_bow_gains[dimension]["Coins"] = round(enemy_coin_reward + giant_coin_reward, 2)
            average_bow_gains[dimension]["Souls"] = round(enemy_reward_bow + giant_soul_reward * boost_bonus, 2)
        if rage:
            enemy_reward_rage = enemy_soul_reward * rage_bonus
            giant_reward_rage = giant_soul_reward * rage_bonus
            average_rage_gains[dimension]["Coins"] = round(enemy_coin_reward + giant_coin_reward, 2)
            average_rage_gains[dimension]["Souls"] = round(enemy_reward_rage + giant_reward_rage, 2)
    return average_base_gains, average_bow_gains, average_rage_gains


@app.route("/")
@cache.cached(timeout=50)
def index():
    return render_template("index.html")


@app.route('/evolutionNames', methods=["GET"])
@cache.cached(timeout=50)
def evolution_names():
    return get_enemy_evolutions()


@app.route('/giantNames', methods=["GET"])
@cache.cached(timeout=50)
def giant_names():
    return get_giant_evolutions()


@app.route('/upgradeNames', methods=["GET"])
@cache.cached(timeout=50)
def upgrade_names():
    return list(get_upgrade_names())


@app.route('/armory', methods=["GET"])
@cache.cached(timeout=50)
def armory():
    with open('./data/get_armory.json', 'r') as fp:
        armory_json = json.loads(fp.read())
    with open('./data/get_armory_types.csv', 'r') as fp:
        reader = csv.reader(fp)
        for line in reader:
            armory_types = line
    with open('./data/get_armory_names.json', 'r') as fp:
        armory_names_json = json.loads(fp.read())
    with open('./data/get_armory_options.json', 'r') as fp:
        armory_options_json = json.loads(fp.read())
    with open('./data/get_armory_levels.json', 'r') as fp:
        armory_levels_json = json.loads(fp.read())
    return [armory_json, armory_types, armory_names_json, armory_options_json, armory_levels_json]


@app.route('/stones', methods=["GET"])
@cache.cached(timeout=50)
def stones():
    with open('./data/get_stone_levels.json', 'r') as fp:
        stone_levels = json.loads(fp.read())
    with open('./data/get_stone_names.csv', 'r') as fp:
        reader = csv.reader(fp)
        for line in reader:
            stone_names = line
    return [stone_names, stone_levels]


@app.route('/randomBoxes', methods=["POST"])
def random_boxes():
    body = request.get_json(force=True)
    random_box = []
    if "RANDOM_BOX" in body:
        random_box = body["RANDOM_BOX"]
    with open('./data/get_random_box.json', 'r') as fp:
        random_box_json = json.loads(fp.read())
    random_box_chance, _ = upgrade_stat_helper(0, random_box_json, random_box)
    return [get_random_box_lower_time(random_box_chance), get_random_box_upper_time(random_box_chance)]


@app.route('/calculateStats', methods=["POST"])
def calculate_stats():
    current_coins = 0
    dimensions, enemy_spawn, giant_spawn, critical_upgrades, boost_souls, bow_souls, giant_souls, rage_souls, \
    enemy_evolutions, giant_evolutions, armory_selection, stone_selection = [], [], [], [], [], [], [], [], [], [], [], []
    body = request.get_json(force=True)
    if "DIMENSIONS" in body:
        dimensions = body["DIMENSIONS"]
    if "ENEMY_SPAWN" in body:
        enemy_spawn = body["ENEMY_SPAWN"]
    if "GIANT_SPAWN" in body:
        giant_spawn = body["GIANT_SPAWN"]
    if "CRITICAL_UPGRADES" in body:
        critical_upgrades = body["CRITICAL_UPGRADES"]
    if "BOOST_SOULS" in body:
        boost_souls = body["BOOST_SOULS"]
    if "BOW_SOULS" in body:
        bow_souls = body["BOW_SOULS"]
    if "GIANT_SOULS" in body:
        giant_souls = body["GIANT_SOULS"]
    if "RAGE_SOULS" in body:
        rage_souls = body["RAGE_SOULS"]
    if "ENEMY_EVOLUTIONS" in body:
        enemy_evolutions = body["ENEMY_EVOLUTIONS"]
    if "GIANT_EVOLUTIONS" in body:
        giant_evolutions = body["GIANT_EVOLUTIONS"]
    if "ARMORY_SELECTION" in body:
        armory_selection = eval(body["ARMORY_SELECTION"])
    if "STONE_SELECTION" in body:
        stone_selection = eval(body["STONE_SELECTION"])
    with open('./data/get_enemies.json', 'r') as fp:
        enemies = json.loads(fp.read())
    with open('./data/get_giants.json', 'r') as fp:
        giants = json.loads(fp.read())
    Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical_Chance, Electric, Fire, Dark, Enemies = calculate_armory_bonuses(
        armory_selection)
    player_speed = 4
    current_enemies, current_coins = get_enemy_stats(current_coins, enemies, enemy_evolutions)
    current_giants, current_coins = get_giant_stats(current_coins, giants, giant_evolutions)
    pattern_spawn, giant_freq, current_coins = get_upgrade_stats(current_coins, enemy_spawn, giant_spawn, Enemies)
    boost_souls_stat, bow_souls_stat, giant_souls_stat, rage_souls_stat, current_coins = \
        get_soul_stats(current_coins, boost_souls, bow_souls, giant_souls, rage_souls)
    critical_chance, critical_souls, current_coins = get_crit_stats(current_coins, critical_upgrades)
    average_patterns = calculate_average_pattern(current_coins, dimensions)
    Critical_Chance += critical_chance
    bow_souls_stat *= Bow_Souls
    Critical_Souls *= critical_souls
    giant_souls_stat *= Giant_Souls

    Ingame_Souls, Bow_Souls_, Critical_Souls_, Souls_, Rage_Souls = calculate_stone_bonuses(stone_selection)
    Souls *= Ingame_Souls * Souls_
    bow_souls_stat *= Bow_Souls_
    Critical_Souls *= Critical_Souls_
    rage_souls_stat += Rage_Souls

    variables = Souls, Critical_Souls, Critical_Chance / 100, Electric, Fire, Dark
    base_gains, bow_gains, rage_gains = calculate_average_gains(average_patterns, current_enemies, current_giants,
                                                                pattern_spawn, giant_freq, boost_souls_stat,
                                                                bow_souls_stat, rage_souls_stat, giant_souls_stat,
                                                                player_speed, variables)
    return [base_gains, bow_gains, rage_gains, bow_souls_stat, rage_souls_stat]


@app.route('/calculateRandomBoxes', methods=["POST"])
def calculate_random_boxes():
    random_box_selection = []
    body = request.get_json(force=True)
    if "RANDOM_BOX_OPTIONS" in body:
        random_box_selection = body["RANDOM_BOX_OPTIONS"]
    random_box_odds = get_box_probabilities(random_box_selection)
    return random_box_odds


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
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
    # critical_upgrades = ["Critical Culling"]
    # bow_souls = ["Soul Grabber", "Augmented Soul Grabber", "Enhanced Soul Grabber", "Blessing of Apollo"]
    # giant_souls = ["Book of Agony", "Wander's Path"]
    # rage_souls = ["Outrage"]
    # enemy_evolutions = ["Hornet", "Black Hornet", "Dark Hornet", "Alpha Worm", "Beta Worm", "Gamma Worm", "Delta Worm",
    #                     "Red Jelly", "Blue Jelly", "Dark Ice Wraith", "Electric Yeti", "Venus Carniplant",
    #                     "Dark Carniplant", "Poison Mushroom", "Blue Milk Mushroom", "Fire Bat", "Black Demon",
    #                     "Corrupted Demon", "Cursed Oak Tree", "Cursed Willow Tree", "Blue Wildfire",
    #                     "Golden Soul Barrel", "Poisonous Gas", "Golden Cobra", "Metal Scorpion"]
    # giant_evolutions = ["Hills' Giant", "Jade Hills' Giant", "Adult Yeti", "Fairy Queen", "Archdemon", "Anubis Warrior"]
    # current_coins = 5e60
    # armory_selection = {'Shield': {'Kishar': {'Option': []}},
    #                     'Armor': {'Adranos': {'Option': ['Excellent', 'Giant Souls', 'Souls'], 'Level': '17'}},
    #                     'Sword': {'Adranos': {'Option': ['Excellent', 'Electric'], 'Level': '16'}},
    #                     'Ring': {"Victor's Ring": {'Level': '10', 'Option': ['Excellent', 'Critical']}},
    #                     'Bow': {'Bat Long Bow': {}}}
    # armory_selection = {}
    # # [Souls * (1 - crit_chance)] + [Souls * crit * crit_souls]
    # Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical_Chance, Electric, Fire, Dark, Enemies = calculate_armory_bonuses(
    #     armory_selection)
    # player_speed = 4
    # current_enemies = get_enemy_stats(get_enemies_json(), enemy_evolutions)
    # current_giants = get_giant_stats(get_giants_json(), giant_evolutions)
    # average_patterns, __ = calculate_average_pattern(current_coins)
    # pattern_spawn, giant_freq = get_upgrade_stats(enemy_spawn, giant_spawn, Enemies)
    # bow_souls_stat, giant_souls_stat, rage_souls_stat = get_soul_stats(bow_souls, giant_souls, rage_souls)
    # critical_chance, critical_souls = get_crit_stats(critical_upgrades)
    # Critical_Chance += critical_chance
    # Critical_Souls *= critical_souls
    # Critical_Chance = 0
    # Critical_Souls = 0
    # variables = Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical_Chance / 100, Electric, Fire, Dark
    # base_gains = calculate_average_base_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
    #                                           giant_freq, giant_souls_stat, player_speed)
    # bow_gains = calculate_average_bow_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
    #                                         giant_freq, bow_souls_stat, player_speed)
    # rage_gains = calculate_average_rage_gains(average_patterns, current_enemies, current_giants, pattern_spawn,
    #                                           giant_freq, giant_souls_stat, rage_souls_stat, player_speed)
    # base_gains_, bow_gains_, rage_gains_ = calculate_average_gains(average_patterns, current_enemies, current_giants,
    #                                                                pattern_spawn, giant_freq, bow_souls_stat,
    #                                                                rage_souls_stat, giant_souls_stat, player_speed,
    #                                                                variables)
