import json
from collections import OrderedDict


def get_armory_json():
    return {
        "Sword": {
            "None": {},
            "Adranos": {
                "Main": ("Souls", 2),
                "Option": [("Excellent", 0), ("Electric", 2)],
                "Levels": list(range(0, 19))
            },
            "Boreas": {
                "Main": ("Fire", 15),
                "Option": [("Excellent", 0), ("Souls", 0.2), ("Fire", 2)],
                "Levels": list(range(0, 19))
            },
            "Kishar": {
                "Option": [("Excellent", 0), ("Enemies", 1)],
                "Levels": list(range(0, 19))
            }
        },
        "Armor": {
            "None": {},
            "Adranos": {
                "Option": [("Excellent", 0), ("Giant Souls", 0.25), ("Souls", 0.7)],
                "Levels": list(range(0, 19))
            },
            "Boreas": {
                "Levels": list(range(0, 19))
            },
            "Kishar": {
                "Option": [("Excellent", 0), ("Enemies", 0.5)],
                "Levels": list(range(0, 19))
            }
        },
        "Shield": {
            "None": {},
            "Adranos": {
                "Main": ("Souls", 1.8),
                "Option": [("Excellent", 0), ("Critical Souls", 0.5), ("Giant Souls", 1.7)],
                "Levels": list(range(0, 19))
            },
            "Boreas": {
                "Main": ("Critical Souls", 4.8),
                "Option": [("Excellent", 0), ("Fire", 0.8)],
                "Levels": list(range(0, 19))
            },
            "Kishar": {
                "Main": ("Critical Souls", 5.5),
                "Option": [("Excellent", 0), ("Giant Souls", 1.5)],
                "Levels": list(range(0, 19))
            }
        },
        "Ring": {
            "None": {},
            "Victor's Ring": {
                "Main": ("Critical Souls", 1),
                "Option": [("Excellent", 0), ("Critical", 0.2)],
                "Levels": list(range(0, 19))
            }
        },
        "Bow": {
            "None": {},
            "Bat Long Bow": {
                "Main": ("Dark", 120)
            },
            "Adranos": {
                "Option": [("Excellent", 0), ("Bow Souls", 3)],
                "Levels": list(range(0, 19))
            },
            "Boreas": {
                "Option": [("Excellent", 0), ("Bow Souls", 2.4)],
                "Levels": list(range(0, 19))
            },
            "Kishar": {
                "Option": [("Excellent", 0), ("Bow Souls", 1.6)],
                "Levels": list(range(0, 19))
            }
        }
    }


def calculate_bonus(stat, level):
    return float(stat) * (int(level) + 1)


def update_bonuses(variables, variable_to_update, multiplier):
    Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical, Electric, Fire, Dark, Enemies = variables
    match variable_to_update:
        case "Souls":
            Souls *= (multiplier / 100) + 1
        case "Bow Souls":
            Bow_Souls *= (multiplier / 100) + 1
        case "Giant Souls":
            Giant_Souls *= (multiplier / 100) + 1
        case "Critical Souls":
            Critical_Souls *= (multiplier / 100) + 1
        case "Critical":
            Critical += multiplier
        case "Electric":
            Electric *= (multiplier / 100) + 1
        case "Fire":
            Fire *= (multiplier / 100) + 1
        case "Dark":
            Dark *= (multiplier / 100) + 1
        case "Enemies":
            Enemies += multiplier
        case other:
            print("something went wrong with " + variable_to_update)
    variables = Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical, Electric, Fire, Dark, Enemies
    return variables


def calculate_armory_bonuses(armory_selection):
    Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical, Electric, Fire, Dark, Enemies = 1, 1, 1, 1, 0, 1, 1, 1, 0
    variables = Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical, Electric, Fire, Dark, Enemies
    armory_json = get_armory_json()
    for item, subtype_info in armory_selection.items():
        for subtype, options_info in subtype_info.items():
            level = 0
            excellent = 1
            if bool(options_info):  # to handle the case where there are no provided options
                if "Level" in options_info:
                    level = options_info["Level"]
                if "Option" in options_info:
                    if "Excellent" in options_info["Option"]:
                        excellent = 1.25
                        options_info["Option"].remove("Excellent")
                    for option in options_info["Option"]:
                        options = armory_json[item][subtype]["Option"]
                        option_name = options[[x for x, y in enumerate(options) if y[0] == option][0]][0]
                        option_stat = options[[x for x, y in enumerate(options) if y[0] == option][0]][1]
                        calculated_bonus = calculate_bonus(option_stat, level) * excellent
                        variables = update_bonuses(variables, option_name, calculated_bonus)
                    # print(item + " " + subtype + " " + option_name + " +" + str(level) + " " + str(calculated_bonus))
            if "Main" in armory_json[item][subtype]:
                main_name = armory_json[item][subtype]["Main"][0]
                main_stat = armory_json[item][subtype]["Main"][1]
                calculated_bonus = calculate_bonus(main_stat, level) * excellent
                # print(item + " " + subtype + " " + main_name + " +" + str(level) + " " + str(calculated_bonus))
                variables = update_bonuses(variables, main_name, calculated_bonus)
    return variables


def get_armory_info():
    armory = get_armory_json()
    armory_types = []
    armory_names = {}
    armory_options = {}
    armory_levels = {}
    for type, sub in armory.items():
        armory_types.append(type)
        armory_names[type] = []
        armory_options[type] = {}
        armory_levels[type] = {}
        for subtype, stats in sub.items():
            armory_names[type].append(subtype)
            armory_options[type][subtype] = []
            armory_levels[type][subtype] = []
            if "Option" in stats:
                for option in stats["Option"]:
                    armory_options[type][subtype].append(option[0])
            if "Levels" in stats:
                for level in stats["Levels"]:
                    armory_levels[type][subtype].append(level)
    return armory, armory_types, armory_names, armory_options, armory_levels


if __name__ == '__main__':
    Example2 = {
        "Shield": {
            "Boreas": {
                "Level": "16"
            }
        }
    }
    Example_Armory = {'Shield': {'Kishar': {'Option': []}},
                      'Armor': {'Adranos': {'Option': ['Excellent', 'Giant Souls', 'Souls'], 'Level': '17'}},
                      'Sword': {'Adranos': {'Option': ['Excellent', 'Electric'], 'Level': '16'}},
                      'Ring': {"Victor's Ring": {'Level': '10', 'Option': ['Excellent']}},
                      'Bow': {'Bat Long Bow': {}}}
    # print(json.dumps(get_armory_json(), indent=4))
    # get_armory_info()
    print(calculate_armory_bonuses(Example2))
