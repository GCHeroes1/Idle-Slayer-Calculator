from Conversion import add_standard_to_dict
import random as random


def get_random_box_json():
    dict = {
        "Mega Random Box": {
            "Cost": float(7.50e21),
            "Benefit": float(50)
        },
        "Roll The Dice": {
            "Cost": "16,500 SP",
            "Benefit": float(20)
        },
        "Pandora's Box": {
            "Cost": float(5.00e54),
            "Benefit": float(8)
        }
    }
    dict = add_standard_to_dict(dict)
    return dict


def get_random_box_event_odds():
    return {"Coins": 1,
            "Frenzy": 0.3,
            "Equipment Bonus": 0.04,
            "OMG": 0.01,
            "Coin Value": 0.05,
            "Dual Randomness": 0.1,
            "Gemstone Rush": 0.12,
            "CpS Multiplier": 0.2,
            "Horde": 0.25,
            "Souls Bonus Multiplier": 0.12
            }


def get_random_box_extra_events():
    return {
        "Souls Bonus Multiplier": {
            "Cost": "5 SP",
        },
        "Dual Randomness": {
            "Cost": "300 SP",
        },
        "Gemstone Rush": {
            "Cost": "10,000 SP",
        },
        "Less Coins More Fun": {
            "Cost": "380 DP",
        }
    }


def get_random_box_lower_time(chance):
    return 38 / (chance / 100 + 1)


def get_random_box_upper_time(chance):
    return 120 / (chance / 100 + 1)


def get_random_box_time(chance):
    upper_bound = 120 / (chance / 100 + 1)
    lower_bound = 38 / (chance / 100 + 1)
    return random.uniform(lower_bound, upper_bound)


if __name__ == '__main__':
    print(get_random_box_json())
