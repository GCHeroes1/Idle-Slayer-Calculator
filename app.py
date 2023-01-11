from flask import Flask, render_template
from Enemies import get_enemies_json
from Upgrades import get_upgrades_json
from Patterns import get_patterns_json
from Giants import get_giants_json
from main import calculate_average_pattern

import copy

app = Flask(__name__)


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
    # enemy
    current_enemies = {}
    current_coins = 0
    for enemy, stats in evolutions.items():
        return_stats = {
            "Dimension": stats["Dimension"],
            "Coins": stats["Coins"],
            "Souls": stats["Souls"]
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
                    if evolution_stats[-1] > current_coins:
                        current_coins = evolution_stats[-1]
        current_enemies[enemy] = return_stats
    return current_enemies, current_coins


def get_patterns(coins):
    patterns_cost = get_upgrades_json()[1]
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
            current_patterns[dimension][enemy] = spawn__
    return current_patterns


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
    # indexes = [0, 4]
    # for index in sorted(indexes, reverse=True):
    #     del giant_names[index]
    #     del giant_info[index]
    return giant_names, giant_info


def get_giant_stats(evolutions, unlocked_enemies):
    # get a list of the selected giants, need to check against the giants list to see whats unlocked
    current_giants = {}
    current_coins = 0
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
                    if evolution_stats[-1] > current_coins:
                        current_coins = evolution_stats[-1]
        current_giants[giant] = return_stats
    return current_giants, current_coins


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(debug=True)
    evolution_names, evolution_info = get_enemy_evolutions()
    enemy_evolutions = ['Hornet', 'Black Hornet']
    current_enemies, current_coins = get_enemy_stats(get_enemies_json(), enemy_evolutions)
    current_patterns = get_patterns(current_coins)
    giant_names, giant_info = get_giant_evolutions()
    giants_unlocked = ["Hills' Giant", 'Adult Yeti', 'Anubis Warrior']
    current_giants, _ = get_giant_stats(get_giants_json(), giants_unlocked)
    average_patterns = calculate_average_pattern(current_patterns)
