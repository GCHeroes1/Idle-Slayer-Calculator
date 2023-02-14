import requests
from bs4 import BeautifulSoup
from Conversion import add_standard_to_dict
import pandas as pd
import re
import json

URL = "https://idleslayer.fandom.com/wiki/Rage_Mode"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_rage_json():
    tb = soup.findAll("table")
    rage = tb[0]
    headers = []
    for i in rage.find_all("th"):
        title = i.text.replace("\n", "")
        headers.append(title)
    rage_data = pd.DataFrame(columns=headers)

    for j in rage.find_all("tr")[1:]:
        row_data = j.find_all("td")
        cost = row_data[1].contents[0].replace("\n", "")
        row = [re.sub(r'\[.*\]', '', i.text.replace("\n", "")) for i in row_data]
        row[1] = cost
        row[2] = re.search('[\d][\d]x', row[2])
        if row[2] is None:
            row[2] = 0
        length = len(rage_data)
        rage_data.loc[length] = row

    rage_data.drop(rage_data[rage_data.Description == 0].index, inplace=True, axis=0)
    rage_data['Description'] = rage_data['Description'].apply(lambda x: x.group(0)[:-1])
    # print(rage_data)
    # rage_data.to_csv("rage_data.csv", index=False)

    dict = {}
    for _, rage in rage_data.iterrows():
        dict[rage["Name"]] = {
            "Cost": rage["Cost"],
            "Benefit": int(rage["Description"]),
        }
    dict["Bad-Tempered"]["Cost"] = "50 B SP"
    dict = add_standard_to_dict(dict)
    with open('./data/get_rage_souls.json', 'w', encoding='utf8') as fp:
        json.dump(dict, fp, ensure_ascii=False)
    return dict


if __name__ == '__main__':
    dict = get_rage_json()

    # print(json.dumps(dict, indent=4))
