import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

URL = "https://idleslayer.fandom.com/wiki/Giants"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_giants_json():
    tb = soup.findAll("table")
    giants = tb[0]
    headers = []
    for i in giants.find_all("th"):
        title = i.text.replace("\n", "")
        headers.append(title)
    giants_data = pd.DataFrame(columns=headers)

    for j in giants.find_all("tr")[1:]:
        row_data = j.find_all("td")
        row = [re.sub(r'\[.*\]', '', i.text.replace("\n", "")) for i in row_data]
        length = len(giants_data)
        giants_data.loc[length] = row

    giants_data.drop(giants_data.index[0], inplace=True)

    giants_data.drop("Image", inplace=True, axis=1)
    giants_data.drop("Drop", inplace=True, axis=1)
    giants_data.drop("UnlockCondition", inplace=True, axis=1)
    # print(enemies_data)
    giants_data.to_csv("giants.csv", index=False)

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

    evolutions_data.drop("Image", inplace=True, axis=1)
    evolutions_data.drop("How To Obtain", inplace=True, axis=1)
    # print(evolutions_data)
    evolutions_data.to_csv("giant_evolutions.csv", index=False)

    dict = {}
    for _, giant in giants_data.iterrows():
        dict[giant["Name"]] = {
            "Dimension": giant["Home Dimension"],
            # "HP": int(giant["HP"]),
            "Coins": int(giant["Coin Reward"]),
            "Souls": int(giant["Soul Reward"]),
            "Evolutions": {}
        }
    for __, evolution in evolutions_data.iterrows():
        dict[evolution["Evolved From"]]["Evolutions"][evolution["Name"]] = {
            # "HP": int(evolution["HP"]),
            "Coins": int(evolution["Coin Reward"]),
            "Souls": int(evolution["Soul Reward"]),
            "Unlock Cost": float(evolution["Unlock Cost"])
        }
    return dict


if __name__ == '__main__':
    dict = get_giants_json()
    print(json.dumps(dict, indent=4))
