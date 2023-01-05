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

    bow_dict = generate_dict(bow_upgrade_data)
    pattern_dict = generate_dict(pattern_upgrade_data)
    spawn_dict = generate_dict(spawn_upgrade_data)
    giant_dict = generate_dict(giant_upgrade_data)

    return bow_dict, pattern_dict, spawn_dict, giant_dict


if __name__ == '__main__':
    bow_dict, pattern_dict, spawn_dict, giant_dict = get_upgrades_json()

    print(json.dumps(bow_dict, indent=4))
    print(json.dumps(pattern_dict, indent=4))
    print(json.dumps(spawn_dict, indent=4))
