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


# def calculate_armory_bonuses(armory_selection):
#     Example_Armory = ["Adranos", ""]
#     Souls, Bow_Souls, Giant_Souls, Critical_Souls, Critical, Electric, Fire, Dark, Enemies = 1, 1, 1, 1, 0, 1, 1, 1, 0

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
    print(json.dumps(get_armory_json(), indent=4))
    get_armory_info()
