import json
from collections import OrderedDict


def get_armory_json():
    return {
        "Sword": {
            "None": {
                "Option": [("None", 0)]
            },
            "Adranos": {
                "Main": ("Souls", 2),
                "Option": [("Electric", 2)]
            },
            "Boreas": {
                "Main": ("Fire", 15),
                "Option": [("Souls", 0.2), ("Fire", 2)]
            },
            "Kishar": {
                "Option": [("Enemies", 1)]
            }
        },
        "Armor": {
            "None": {
                "Option": [("None", 0)]
            },
            "Adranos": {
                "Option": [("Giant Souls", 0.25), ("Souls", 0.7)]
            },
            "Boreas": {},
            "Kishar": {
                "Option": [("Enemies", 0.5)]
            }
        },
        "Shield": {
            "None": {
                "Option": [("None", 0)]
            },
            "Adranos": {
                "Main": ("Souls", 1.8),
                "Option": [("Critical Souls", 0.5), ("Giant Souls", 1.7)]
            },
            "Boreas": {
                "Main": ("Critical Souls", 4.8),
                "Option": [("Fire", 0.8)]
            },
            "Kishar": {
                "Main": ("Critical Souls", 5.5),
                "Option": [("Giant Souls", 1.5)]
            }
        },
        "Ring": {
            "None": {
                "Option": [("None", 0)]
            },
            "Victor's Ring": {
                "Main": ("Critical Souls", 1),
                "Option": [("Critical", 0.2)]
            }
        },
        "Bow": {
            "None": {
                "Option": [("None", 0)]
            },
            "Bat Long Bow": {
                "Main": ("Dark", 120)
            },
            "Adranos": {
                "Option": [("Bow Souls", 3)]
            },
            "Boreas": {
                "Option": [("Bow Souls", 2.4)]
            },
            "Kishar": {
                "Option": [("Bow Souls", 1.6)]
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
    for type, sub in armory.items():
        armory_types.append(type)
        armory_names[type] = []
        armory_options[type] = {}
        for subtype, stats in sub.items():
            armory_names[type].append(subtype)
            armory_options[type][subtype] = []
            if "Option" in stats:
                for option in stats["Option"]:
                    armory_options[type][subtype].append(option[0])
    return armory, armory_types, armory_names, armory_options


if __name__ == '__main__':
    print(json.dumps(get_armory_json(), indent=4))
    get_armory_info()
