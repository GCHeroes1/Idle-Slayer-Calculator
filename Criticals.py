import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

URL = "https://idleslayer.fandom.com/wiki/Critical_Culling"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_crit_json():
    tb = soup.findAll("table")
    crit = tb[0]
    headers = []
    for i in crit.find_all("th"):
        title = i.text.replace("\n", "")
        headers.append(title)
    crit_data = pd.DataFrame(columns=headers)

    for j in crit.find_all("tr")[1:]:
        row_data = j.find_all("td")
        cost = row_data[2].contents[0].replace("\n", "")
        row = [re.sub(r'\[.*\]', '', i.text.replace("\n", "")) for i in row_data]
        row[2] = cost
        # row[2] = re.search('[\d][\d]x', row[2])
        # if row[2] is None:
        #     row[2] = 0
        length = len(crit_data)
        crit_data.loc[length] = row

    crit_data = crit_data.tail(-1)
    crit_data.drop("Image", inplace=True, axis=1)
    crit_data.drop("Notes", inplace=True, axis=1)
    # crit_data.drop(crit_data[crit_data.Description == 0].index, inplace=True, axis=0)
    # crit_data['Description'] = crit_data['Description'].apply(lambda x: x.group(0)[:-1])
    # print(rage_data)
    # rage_data.to_csv("rage_data.csv", index=False)

    dict = {}
    dict["Critical Culling"] = {"Cost": "150,000 SP",
                                "Critical": int(15),
                                "Critical Souls": int(100)}
    for _, crit in crit_data.iterrows():
        if "chance" in crit["Description"]:
            dict[crit["Name"]] = {
                "Cost": crit["Cost"],
                "Critical": int(crit["Description"][-3:-2]),
            }
        elif "Souls" in crit["Description"]:
            dict[crit["Name"]] = {
                "Cost": crit["Cost"],
                "Critical Souls": int(crit["Description"][-4:-2]),
            }
    return dict


if __name__ == '__main__':
    dict = get_crit_json()
    print(json.dumps(dict, indent=4))
