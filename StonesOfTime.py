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
            "Levels": list(range(0, 35))
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
            "Levels": list(range(0, 35))
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
            "Levels": list(range(0, 35))
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
            "Levels": list(range(0, 35))
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
    match stone:
        case "Activity":
            Ingame_Souls *= get_stat_multiplier(level, "Ingame Souls") / 100 + 1
            Bow_Souls *= get_stat_multiplier(level, "Bow Souls") / 100 + 1
        case "Idle":
            Critical_Souls *= get_stat_multiplier(level, "Critical Souls") / 100 + 1
        case "Hope":
            Souls *= get_stat_multiplier(level, "Souls") / 100 + 1
        case "Rage":
            Rage_Souls += get_stat_multiplier(level, "Rage Souls")
        case other:
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


if __name__ == '__main__':
    USP_allocation = {
        "Idle": "17",
        "Activity": "32",
        "Hope": "33",
        "Rage": "19"
    }
    print(calculate_stone_bonuses(USP_allocation))
    # print(get_sot_info())
