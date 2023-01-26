import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

from Conversion import add_standard_to_dict

URL = "https://idleslayer.fandom.com/wiki/Enemies"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_enemies_json():
    tb = soup.findAll("table")
    enemies = tb[0]
    headers = []
    for i in enemies.find_all("th"):
        title = i.text.replace("\n", "")
        headers.append(title)
    enemies_data = pd.DataFrame(columns=headers)

    for j in enemies.find_all("tr")[1:]:
        row_data = j.find_all("td")
        dimension = row_data[2].contents[::2]
        row = [re.sub(r'\[.*\]', '', i.text.replace("\n", "")) for i in row_data]
        for index, dim in enumerate(dimension):
            if "\n" in dim:
                dimension[index] = dim.replace("\n", "")
            if dimension[index] == "":
                dimension.remove("")
        row[2] = dimension
        length = len(enemies_data)
        enemies_data.loc[length] = row

    enemies_data.drop(enemies_data.index[11], inplace=True)

    enemies_data.drop("Image", inplace=True, axis=1)
    enemies_data.drop("Evolutions", inplace=True, axis=1)
    enemies_data.drop("Enemy Type", inplace=True, axis=1)
    enemies_data.drop("Drop", inplace=True, axis=1)
    # print(enemies_data)
    # enemies_data.to_csv("enemies.csv", index=False)

    evolutions = tb[1]
    headers = []
    for i in evolutions.find_all("th"):
        title = re.sub(r'\(.*\)', '', i.text.replace("\n", ""))
        headers.append(title)
    evolutions_data = pd.DataFrame(columns=headers)

    for j in evolutions.find_all("tr")[1:]:
        row_data = j.find_all("td")
        cost = row_data[6].contents[0]
        row = [re.sub(r'\(.*\)', '', re.sub(r'\[.*\]', '', i.text.replace("\n", ""))) for i in row_data]
        row[6] = cost
        length = len(evolutions_data)
        evolutions_data.loc[length] = row

    evolutions_data.drop(evolutions_data.index[21:23], inplace=True)

    evolutions_data.drop("Image", inplace=True, axis=1)
    evolutions_data.drop("How To Obtain", inplace=True, axis=1)
    # print(evolutions_data)
    # evolutions_data.to_csv("enemy_evolutions.csv", index=False)

    dict = {}
    for _, enemy in enemies_data.iterrows():
        dict[enemy["Enemy"]] = {
            "Dimension": enemy["Home Dimension(s)"],
            "Coins": int(enemy["Coin Reward"]),
            "Souls": int(enemy["Soul Reward"]),
            "Evolutions": {}
        }
    for __, evolution in evolutions_data.iterrows():
        dict[evolution["Evolved From"]]["Evolutions"][evolution["Name"]] = {
            "Type": evolution["Type"],
            "Coins": int(evolution["Coin Reward"]),
            "Souls": int(evolution["Soul Reward"]),
            "Cost": float(evolution["Unlock Cost"])
        }
    dict = add_standard_to_dict(dict)

    return dict


if __name__ == '__main__':
    dict = get_enemies_json()
    # print(json.dumps(dict, indent=4))
