import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import copy

patterns_new = {
    "Hills": {
        1: [["Wasp"],
            ["Wasp", "Wasp"]],
        2: [["Wasp", "Wasp", "Wasp"],
            ["Wasp", "Wasp", "Wasp"],
            ["Wasp", "Wasp", "Wasp"],
            ["Wasp", "Wasp", "Wasp", "Wasp"],
            ["Worm"],
            ["Worm", "Worm"],
            ["Worm", "Worm", "Worm", "Worm", "Worm"]],
        3: [["Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp"],
            ["Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp"],
            ["Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm"]]

    },
    "Jungle": {
        1: [[]],
        2: [["Wasp", "Wasp", "Wasp"],
            ["Wasp", "Wasp", "Wasp"],
            ["Mushroom", "Mushroom", "Mushroom", "Mushroom"],
            ["Carniplant", "Carniplant"]],
        3: [["Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp"],
            ["Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp", "Wasp"],
            ["Carniplant", "Carniplant", "Carniplant"],
            ["Mushroom", "Mushroom", "Mushroom", "Mushroom", "Mushroom", "Mushroom"]]
    },
    "Haunted Castle": {
        1: [[]],
        2: [["Demon"],
            ["Worm"],
            ["Worm", "Worm"],
            ["Bat", "Bat", "Bat", "Bat"],
            ["Worm", "Worm", "Worm", "Worm", "Worm"],
            ["Bat", "Bat", "Bat", "Bat", "Bat"]],
        3: [["Demon", "Demon"],
            ["Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm"],
            ["Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat"]]
    },
    "Modern City": {
        1: [[]],
        2: [["Worm", "Worm"],
            ["Worm", "Worm", "Worm", "Worm", "Worm"],
            ["Bat", "Bat", "Bat", "Bat"],
            ["Bat", "Bat", "Bat", "Bat", "Bat"],
            ["Jelly", "Jelly"],
            ["Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly"]],
        3: [["Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm", "Worm"],
            ["Jelly", "Jelly", "Jelly"],
            ["Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly"],
            ["Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat", "Bat"]]
    },
    "Frozen Fields": {
        1: [[]],
        2: [["Jelly", "Young Yeti", "Young Yeti"],
            ["Young Yeti"],
            ["Young Yeti", "Young Yeti", "Young Yeti"],
            ["Ice Wraith", "Ice Wraith", "Ice Wraith"]],
        3: [["Young Yeti", "Young Yeti", "Young Yeti"],
            ["Young Yeti", "Young Yeti", "Young Yeti", "Young Yeti"],
            ["Ice Wraith", "Ice Wraith", "Ice Wraith", "Ice Wraith", "Ice Wraith", "Ice Wraith"]]
    },
    "Factory": {
        1: [[]],
        2: [["Soul Barrel"],
            ["Soul Barrel", "Soul Barrel", "Soul Barrel"],
            ["Soul Barrel", "Soul Barrel", "Soul Barrel"],
            ["Toxic Gas", "Toxic Gas", "Toxic Gas"],
            ["Toxic Gas", "Toxic Gas", "Toxic Gas"],
            ["Toxic Gas", "Toxic Gas", "Toxic Gas", "Toxic Gas"],
            ["Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly"]],
        3: [["Soul Barrel", "Soul Barrel", "Soul Barrel", "Soul Barrel", "Soul Barrel"],
            ["Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly", "Jelly"]]
    },
    "Mystic Valley": {
        1: [[]],
        2: [["Cursed Tree", "Cursed Tree"],
            ["Cursed Tree", "Cursed Tree"],
            ["Cursed Tree", "Cursed Tree"],
            ["Wildfire"],
            ["Wildfire", "Wildfire"],
            ["Wildfire", "Wildfire", "Wildfire"],
            ["Mushroom"],
            ["Mushroom", "Mushroom", "Mushroom", "Mushroom"],
            ["Mushroom", "Mushroom", "Mushroom", "Mushroom", "Cursed Tree", "Cursed Tree"]],
        3: [["Cursed Tree", "Cursed Tree", "Cursed Tree", "Cursed Tree"],
            ["Wildfire", "Wildfire", "Wildfire", "Wildfire", "Wildfire", "Wildfire"],
            ["Wildfire", "Wildfire", "Wildfire", "Wildfire", "Wildfire", "Wildfire", "Wildfire", "Wildfire"]]
    },
    "Hot Desert": {
        1: [["Scorpion"],
            ["Cobra", "Cobra", "Cobra"],
            ["Vulture", "Vulture", "Vulture", "Vulture"]],
        2: [["Cobra", "Cobra", "Scorpion"],
            ["Vulture", "Vulture", "Vulture", "Vulture", "Vulture", "Vulture"]],
        3: [["Cobra", "Cobra", "Scorpion", "Scorpion", "Scorpion"],
            ["Vulture", "Vulture", "Vulture", "Vulture", "Vulture", "Vulture", "Vulture", "Vulture"]]
    },
    "Funky Space": {
        1: [["Funkloud", "Funkloud", "Funkloud", "Funkloud", "Funkloud"],
            ["Star Note", "Star Note", "Star Note", "Star Note", "Star Note", "Star Note"],
            ["Star Note", "Star Note", "Star Note", "Star Note", "Star Note", "Star Note"],
            ["Star Note", "Star Note", "Star Note", "Star Note", "Star Note", "Star Note"]],
        2: [[]],
        3: [[]]
    },
}

URL = "https://idleslayer.fandom.com/wiki/Patterns"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_dimension_patterns_json():
    # tb = soup.findAll("table")
    # patterns = tb[3:]
    # headers = ["Enemy"]
    #
    # for i in patterns[0].find_all("th"):
    #     title = i.text.replace("\n", "")
    #     headers.append(title)
    # pattern_data = pd.DataFrame(columns=headers)
    #
    # for pattern in patterns:
    #     caption = re.sub(r'\(.*\)', '', pattern.find("caption").next)[:-2]
    #     for j in pattern.find_all("tr")[1:]:
    #         row_data = j.find_all("td")
    #         row = [caption] + [re.sub(r'\(.*\)', '', re.sub(r'\[.*\]', '', i.text.replace("\n", ""))) for i in row_data]
    #         length = len(pattern_data)
    #         pattern_data.loc[length] = row
    #
    # pattern_data.drop("Formation", inplace=True, axis=1)
    # # print(pattern_data)
    # # pattern_data.to_csv("patterns.csv", index=False)
    #
    # dict = {}
    # for _, pattern in pattern_data.iterrows():
    #     maps = pattern["Map(s)"].split(", ")
    #     for map in maps:
    #         if map not in dict:
    #             dict[map] = {}
    #         if pattern["Enemy"] not in dict[map]:
    #             dict[map][pattern["Enemy"]] = []
    #         dict[map][pattern["Enemy"]].append((int(pattern["Enemies"]), int(pattern["Level"])))
    #
    # with open('./data/get_dimension_patterns_old.json', 'w', encoding='utf8') as fp:
    #     json.dump(dict, fp, ensure_ascii=False)
    with open('./data/get_dimension_patterns.json', 'w', encoding='utf8') as fp:
        json.dump(patterns_new, fp, ensure_ascii=False)
    return patterns_new


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
        if dimension not in unlocked_dimensions:
            del current_patterns[dimension]
        else:
            for level, pattern in dimension_pattern.items():
                if int(level) > spawn_level:
                    del (current_patterns[dimension][level])

    average_patterns = {}
    totals = {}
    for dimension in unlocked_dimensions:
        average_patterns[dimension] = {}
        totals[dimension] = {}
        for level, patterns in current_patterns[dimension].items():
            for pattern in patterns:
                if totals[dimension].get("Pattern Count") is None:
                    totals[dimension]["Pattern Count"] = 0
                if len(current_patterns[dimension][level][0]) != 0:
                    totals[dimension]["Pattern Count"] += 1
                for enemy in pattern:
                    if totals[dimension].get(enemy) is None:
                        totals[dimension][enemy] = 0
                    totals[dimension][enemy] += 1
    for dimension, info in totals.items():
        for enemy, count in info.items():
            if enemy != "Pattern Count":
                average_patterns[dimension][enemy] = {
                    "Average": count / totals[dimension]["Pattern Count"]
                }
    return average_patterns


if __name__ == '__main__':
    dict = get_dimension_patterns_json()
    dict2 = calculate_average_pattern(1e100, ["Jungle"])
    # print(json.dumps(dict, indent=4))
    print(json.dumps(dict2, indent=4))
