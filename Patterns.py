import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

URL = "https://idleslayer.fandom.com/wiki/Patterns"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_patterns_json():
    tb = soup.findAll("table")
    patterns = tb[3:]
    headers = ["Enemy"]

    for i in patterns[0].find_all("th"):
        title = i.text.replace("\n", "")
        headers.append(title)
    pattern_data = pd.DataFrame(columns=headers)

    for pattern in patterns:
        caption = re.sub(r'\(.*\)', '', pattern.find("caption").next)[:-2]
        for j in pattern.find_all("tr")[1:]:
            row_data = j.find_all("td")
            row = [caption] + [re.sub(r'\(.*\)', '', re.sub(r'\[.*\]', '', i.text.replace("\n", ""))) for i in row_data]
            length = len(pattern_data)
            pattern_data.loc[length] = row

    pattern_data.drop("Formation", inplace=True, axis=1)
    # print(pattern_data)
    # pattern_data.to_csv("patterns.csv", index=False)

    dict = {}
    for _, pattern in pattern_data.iterrows():
        maps = pattern["Map(s)"].split(", ")
        for map in maps:
            if map not in dict:
                dict[map] = {}
            if pattern["Enemy"] not in dict[map]:
                dict[map][pattern["Enemy"]] = []
            dict[map][pattern["Enemy"]].append((int(pattern["Enemies"]), int(pattern["Level"])))
    return dict


if __name__ == '__main__':
    dict = get_patterns_json()

    print(json.dumps(dict, indent=4))
