import requests
from bs4 import BeautifulSoup
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


def get_upgrades_json():
    tb = soup.findAll("table")
    bowSoulUpgrades = tb[12]
    patternUpgrades = tb[20]
    spawnUpgrades = tb[21]
    giantUpgrades = tb[25]

    # # pattern_data.to_csv("patterns.csv", index=False)
    bow_upgrade_data = generate_dataframe(bowSoulUpgrades)
    pattern_upgrade_data = generate_dataframe(patternUpgrades)
    spawn_upgrade_data = generate_dataframe(spawnUpgrades)
    giant_upgrade_data = generate_dataframe(giantUpgrades)
    giant_upgrade_data.drop(giant_upgrade_data.index[2], inplace=True)

    bow_souls_dict = generate_dict(bow_upgrade_data)
    pattern_dict = generate_dict(pattern_upgrade_data)
    spawn_dict = generate_dict(spawn_upgrade_data)
    giant_dict = generate_dict(giant_upgrade_data)
    bow_souls_dict["Wind Waker"] = {
        # "Cost": 0,  # 200 DP
        "Cost": "200 DP",  # 200 DP
        "Benefit": int(100)
    }
    bow_souls_dict["Dark Projectiles"] = {
        # "Cost": 0,  # 140 DP
        "Cost": "140 DP",  # 140 DP
        "Benefit": int(100)
    }
    spawn_dict["Bring Hell"] = {
        "Cost": 0,  # 600 SP
        "Cost": "600 SP",  # 600 SP
        "Benefit": int(20)
    }
    spawn_dict["Doomed"] = {
        "Cost": 0,  # 2,500 SP
        "Cost": "2,500 SP",  # 2,500 SP
        "Benefit": int(30)
    }
    spawn_dict["Reincarnation"] = {
        # "Cost": 0,  # 2.5B SP
        "Cost": "2.5B SP",  # 2.5B SP
        "Benefit": int(25)
    }
    giant_dict["Big Troubles"] = {
        # "Cost": 0,  # 15 DP
        "Cost": "15 DP",  # 15 DP
        "Benefit": int(15)
    }
    giant_souls_dict = {
        "Book of Agony": {
            "Cost": float(2.00e40),
            "Benefit": int(60)
        },
        "Wander's Path": {
            # "Cost": 0,  # 1T SP
            "Cost": "1T SP",  # 1T SP
            "Benefit": int(400)
        }
    }

    return bow_souls_dict, giant_souls_dict, pattern_dict, spawn_dict, giant_dict


if __name__ == '__main__':
    bow_dict, pattern_dict, spawn_dict, giant_dict = get_upgrades_json()

    print(json.dumps(bow_dict, indent=4))
    print(json.dumps(pattern_dict, indent=4))
    print(json.dumps(spawn_dict, indent=4))
