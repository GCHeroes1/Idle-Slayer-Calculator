import requests
from bs4 import BeautifulSoup
from Conversion import add_standard_to_dict
import pandas as pd
import re
import json

URL = "https://idleslayer.fandom.com/wiki/Upgrades"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def generate_dataframe(upgradesTable):
    headers = []

    for i in upgradesTable.find_all("th"):
        title = re.sub(r'\(.*\)', '', i.text.replace("\n", ""))
        headers.append(title)
    data = pd.DataFrame(columns=headers)

    for j in upgradesTable.find_all("tr")[1:]:
        row_data = j.find_all("td")

        cost = row_data[1].contents[0]
        row = [re.sub(r'\(.*\)', '', re.sub(r'\[.*\]', '', i.text.replace("\n", ""))) for i in row_data]
        row[1] = cost
        row[2] = re.sub('\D', '', row[2])
        length = len(data)
        data.loc[length] = row

    data.drop("Unlock Condition", inplace=True, axis=1)
    return data


def generate_dict(dataframe):
    dict = {}
    for _, data in dataframe.iterrows():
        if len(data["Benefit"]) == 0:
            data["Benefit"] = _ + 1
        dict[data["Name"]] = {
            "Cost": float(data["Cost"]),
            "Benefit": int(data["Benefit"])
        }
    return dict


def generate_costs_dict(dataframe):
    dict = {}
    for _, data in dataframe.iterrows():
        dict[data["Name"]] = {
            "Cost": str(data["Cost"]),
        }
    return dict


def get_giant_costs_json():
    headers = soup.findAll("h3")
    for item in headers:
        table = item.findNext("table")
        if "Giant Unlocks" in item.contents[0]:
            giantUnlock = generate_dataframe(table)
    giant_cost_dict = generate_costs_dict(giantUnlock)
    with open('./data/get_giant_cost.json', 'w') as fp:
        json.dump(giant_cost_dict, fp)
    return giant_cost_dict


def get_upgrades_json():
    headers = soup.findAll("h3")
    for item in headers:
        table = item.findNext("table")
        if "Bow Soul Upgrades" in item.contents[0]:
            bowSoul = generate_dataframe(table)
        elif "Enemy Pattern Upgrades" in item.contents[0]:
            enemyPattern = generate_dataframe(table)
        elif "Enemy Spawn Upgrades" in item.contents[0]:
            enemySpawn = generate_dataframe(table)
        elif "Giant Spawn Upgrades" in item.contents[0]:
            giantSpawn = generate_dataframe(table)
            giantSpawn.drop(giantSpawn.index[2], inplace=True)

    bow_souls_dict = generate_dict(bowSoul)
    pattern_dict = generate_dict(enemyPattern)
    spawn_dict = generate_dict(enemySpawn)
    giant_dict = generate_dict(giantSpawn)
    bow_souls_dict["Wind Waker"] = {
        "Cost": "200 DP",
        "Benefit": int(100)
    }
    bow_souls_dict["Dark Projectiles"] = {
        "Cost": "140 DP",
        "Benefit": int(100)
    }
    spawn_dict["Bring Hell"] = {
        "Cost": "600 SP",
        "Benefit": int(20)
    }
    spawn_dict["Doomed"] = {
        "Cost": "2,500 SP",
        "Benefit": int(30)
    }
    spawn_dict["Reincarnation"] = {
        "Cost": "2.5 B SP",
        "Benefit": int(25)
    }
    giant_dict["Big Troubles"] = {
        "Cost": "45 DP",
        "Benefit": int(15)
    }
    giant_souls_dict = {
        "Book of Agony": {
            "Cost": float(2.00e40),
            "Benefit": int(60)
        },
        "Wander's Path": {
            "Cost": "1 T SP",
            "Benefit": int(400)
        }
    }
    boost_souls_dict = {
        "Boost Kill": {
            "Cost": "10 SP",
            "Benefit": int(100)
        },
        "Augmented Boost Kill": {
            "Cost": "100,000 SP",
            "Benefit": int(100)
        }
    }
    boost_souls_dict = add_standard_to_dict(boost_souls_dict)
    bow_souls_dict = add_standard_to_dict(bow_souls_dict)
    giant_souls_dict = add_standard_to_dict(giant_souls_dict)
    pattern_dict = add_standard_to_dict(pattern_dict)
    spawn_dict = add_standard_to_dict(spawn_dict)
    giant_dict = add_standard_to_dict(giant_dict)

    with open('./data/get_boost_souls.json', 'w') as fp:
        json.dump(boost_souls_dict, fp)
    with open('./data/get_bow_souls.json', 'w') as fp:
        json.dump(bow_souls_dict, fp)
    with open('./data/get_giant_souls.json', 'w') as fp:
        json.dump(giant_souls_dict, fp)
    with open('./data/get_patterns_cost.json', 'w') as fp:
        json.dump(pattern_dict, fp)
    with open('./data/get_enemy_spawn.json', 'w') as fp:
        json.dump(spawn_dict, fp)
    with open('./data/get_giant_spawn.json', 'w') as fp:
        json.dump(giant_dict, fp)
    return boost_souls_dict, bow_souls_dict, giant_souls_dict, pattern_dict, spawn_dict, giant_dict


if __name__ == '__main__':
    boost_souls_dict, bow_souls_dict, giant_souls_dict, pattern_dict, spawn_dict, giant_dict = get_upgrades_json()
    giant_cost_dict = get_giant_costs_json()

    # print(json.dumps(bow_souls_dict, indent=4))
    # print(json.dumps(pattern_dict, indent=4))
    # print(json.dumps(spawn_dict, indent=4))
