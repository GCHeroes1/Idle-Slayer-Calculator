import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

from Conversion import add_standard_to_dict

URL = "https://idleslayer.fandom.com/wiki/Portals_and_Dimensions"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def get_dimension_json():
    tb = soup.findAll("table")
    dimension = tb[1]
    headers = []
    for i in dimension.find_all("th"):
        title = i.text.replace("\n", "")
        headers.append(title)
    dimension_data = pd.DataFrame(columns=headers)

    for j in dimension.find_all("tr")[1:]:
        row_data = j.find_all("td")
        cost = row_data[1].contents[0].replace("\n", "")
        row = [re.sub(r'\[.*\]', '', i.text.replace("\n", "")) for i in row_data]
        row[1] = cost
        length = len(dimension_data)
        dimension_data.loc[length] = row

    dict = {}
    for _, dimension in dimension_data.iterrows():
        if "Use the Portal" in dimension["Description"]:
            dict[dimension["Name"]] = {
                "Cost": dimension["Cost"],
            }
    dict["Hot Desert"]["Cost"] = "5 SP, after UA"
    dict = add_standard_to_dict(dict)
    return dict


if __name__ == '__main__':
    dict = get_dimension_json()
    print(json.dumps(dict, indent=4))
