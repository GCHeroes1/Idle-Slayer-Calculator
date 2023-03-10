from Conversion import add_standard_to_dict
import random as random
import json
import copy


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
    with open('./data/get_random_box.json', 'w', encoding='utf8') as fp:
        json.dump(dict, fp, ensure_ascii=False)
    return dict


def get_random_box_event_odds_json():  # could be obtained from the wiki, but its never updated, never changes
    dict = {"Coins": 1,
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
    with open('./data/get_random_box_event_odds.json', 'w', encoding='utf8') as fp:
        json.dump(dict, fp, ensure_ascii=False)
    return dict


def get_random_box_extra_options_json():
    dict = {
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
        },
        "In a Bonus Stage": {
            "Cost": "2.50e9",
        }
    }
    dict = add_standard_to_dict(dict)
    with open('./data/get_random_box_extra_options.json', 'w', encoding='utf8') as fp:
        json.dump(dict, fp, ensure_ascii=False)
    return dict


def get_random_box_lower_time(chance):
    return 38 / (chance / 100 + 1)


def get_random_box_upper_time(chance):
    return 120 / (chance / 100 + 1)


def get_random_box_time(chance):
    upper_bound = 120 / (chance / 100 + 1)
    lower_bound = 38 / (chance / 100 + 1)
    return random.uniform(lower_bound, upper_bound)


class Distribution:
    def __init__(self):
        self.dist = {}
        self.empty = 1
        with open('./data/get_random_box_event_odds.json', 'r') as fp:
            self.random_box_bonuses = json.loads(fp.read())
        for key, box in self.random_box_bonuses.items():
            self.dist[key] = 0

        self.update()

    def update(self):
        self.empty = 1
        for key, box in self.random_box_bonuses.items():
            self.empty -= self.dist[key]

    def add(self, other):
        for key, box in self.random_box_bonuses.items():
            self.dist[key] += other.dist[key]

    def divide(self, scalar):
        for key, box in self.random_box_bonuses.items():
            self.dist[key] /= scalar

    def normalize(self):
        self.divide(1 - self.empty)


def calculate_distribution(distribution_cache, box_set):
    set_names = "".join(list(box_set.keys()))
    if set_names in distribution_cache:
        return distribution_cache[set_names]

    new_dist = Distribution()
    # 1. If set has only 1 element, calculate it.
    if len(box_set) == 1:
        for key, chance in box_set.items():
            new_dist.dist[key] = chance
            new_dist.update()
        distribution_cache[set_names] = new_dist
        return new_dist

    # 2. Otherwise, calculate it in function of the subsets
    #
    # Idea: take each element, pretend it's the last one in the shuffle.
    # The resulting distribution is the same as that of the reduced set, except
    # probability of the last element is its base probability * reduced.empty.
    #
    # Calculating the average after making each element of the set be the last
    # gives the final distribution.
    for key, chance in box_set.items():
        reduced_set = box_set.copy()
        reduced_set.pop(key)
        reduced = calculate_distribution(distribution_cache, reduced_set)
        new_dist.add(reduced)
        new_dist.dist[key] += chance * reduced.empty

    new_dist.divide(len(box_set))
    new_dist.update()
    distribution_cache[set_names] = new_dist
    # print(len(distribution_cache))
    return new_dist


def get_box_probabilities(selected_options):
    with open('./data/get_random_box_event_odds.json', 'r') as fp:
        current_events = json.loads(fp.read())
    current_events_copy = copy.deepcopy(current_events)
    with open('./data/get_random_box_extra_options.json', 'r') as fp:
        extra_options = json.loads(fp.read())
    current_events["Coins"] = 0.9
    current_events["Frenzy"] = 0
    current_events["Horde"] = 0
    for key, value in extra_options.items():
        if key not in selected_options:
            if key == "Less Coins More Fun":
                current_events["Coins"] = current_events_copy["Coins"]
            elif key == "In a Bonus Stage":
                current_events["Frenzy"] = current_events_copy["Frenzy"]
                current_events["Horde"] = current_events_copy["Horde"]
            else:
                current_events.pop(key)
    distribution = calculate_distribution({}, current_events)
    distribution.normalize()
    return distribution.dist


if __name__ == '__main__':
    dict = get_random_box_json()
    dict = get_random_box_event_odds_json()
    dict = get_random_box_extra_options_json()

    current = ["Souls Bonus Multiplier", "Dual Randomness", "Less Coins More Fun"]

    # print(get_box_probabilities(current))
    # print(json.dumps(dict, indent=4))
