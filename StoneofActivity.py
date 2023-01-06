import numpy as np

stoneOfActivity = {
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
    }
}


def calculate_bow_bonus(souls, decrease, min, USP, current_bonus):
    if USP == 0:
        return current_bonus
    if USP == 1:
        return USP * souls
    else:
        return max(souls - (decrease * (USP - 1)), min) + calculate_bow_bonus(souls, decrease, min, USP - 1,
                                                                              current_bonus)


def get_soa_bow_bonus(USP):
    souls_per_USP = stoneOfActivity["Bow Souls"]["Per USP"]
    decrease_per_USP = stoneOfActivity["Bow Souls"]["Decrease"]
    minimum = stoneOfActivity["Bow Souls"]["Minimum"]
    multiplier = 1
    if USP != 0:
        multiplier *= 2
    if USP > 25:
        multiplier *= 2
    return multiplier * (calculate_bow_bonus(souls_per_USP, decrease_per_USP, minimum, USP, 0) / 100 + 1)


if __name__ == '__main__':
    for i in range(0, 100):
        print(i, get_soa_bow_bonus(i))
