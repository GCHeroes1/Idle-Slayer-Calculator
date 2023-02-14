import requests
from bs4 import BeautifulSoup
from Conversion import add_standard_to_dict
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
        length = len(crit_data)
        crit_data.loc[length] = row

    crit_data = crit_data.tail(-1)
    crit_data.drop("Image", inplace=True, axis=1)
    crit_data.drop("Notes", inplace=True, axis=1)

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

    dict = add_standard_to_dict(dict)
    with open('./data/get_crit.json', 'w', encoding='utf8') as fp:
        json.dump(dict, fp, ensure_ascii=False)
    return dict


if __name__ == '__main__':
    dict = get_crit_json()

    # print(json.dumps(dict, indent=4))
