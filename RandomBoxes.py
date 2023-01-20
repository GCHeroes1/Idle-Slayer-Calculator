from Conversion import convert_standard_to_exponential
import random as random


def get_random_box_json():
    return {
        "Mega Random Box": {
            "Cost": float(7.50e21),
            "Benefit": float(50)
        },
        "Roll The Dice": {
            "Cost": convert_standard_to_exponential("10 No"),
            "Benefit": float(20)
        },
        "Pandora's Box": {
            "Cost": float(5.00e54),
            "Benefit": float(8)
        }
    }


def get_random_box_time(chance):
    upper_bound = 120 / (chance / 100 + 1)
    lower_bound = 38 / (chance / 100 + 1)
    return random.uniform(lower_bound, upper_bound)


if __name__ == '__main__':
    print(get_random_box_time(0))
