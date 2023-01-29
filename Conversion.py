import math

standardNotation = ["M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "De", "Ud", "Dd", "Td", "Qt", "Qd", "Sd",
                    "St", "Od", "Nd", "Vg", "Uv", "Dv", "Tv", "Qav", "Qiv", "Sxv", "Spv", "Ocv"]
exponentials = [float("1e6"), float("1e9"), float("1e12"), float("1e15"), float("1e18"), float("1e21"), float("1e24"),
                float("1e27"), float("1e30"), float("1e33"), float("1e36"), float("1e39"), float("1e42"), float("1e45"),
                float("1e48"), float("1e51"), float("1e54"), float("1e57"), float("1e60"), float("1e63"), float("1e66"),
                float("1e69"), float("1e72"), float("1e75"), float("1e78"), float("1e81"), float("1e84"), float("1e87")]


def convert_standard_to_exponential(standard):
    abbreviation = str(standard).split(' ')[1]
    coins = float(str(standard).split(' ')[0])
    index = standardNotation.index(abbreviation)

    return coins * exponentials[index]


def convert_exponential_to_standard(exponential):
    if "e" in str(exponential):
        try:
            exponent = str(exponential).split('e')[1]
            base = str(exponential).split('e')[0]
            exponent_div_3 = float(exponent) / 3
            floor = math.floor(exponent_div_3)
            difference = int(round(((exponent_div_3 - floor) * 3), 0))
            lower_exponential = exponentials[floor - 2]
            index = exponentials.index(lower_exponential)
            abbreviation = standardNotation[index]
            final_number = float(base) * (1 * (10 ** difference))
            final_string = str(final_number) + " " + abbreviation
            return final_string
        except:
            return str(exponential)
    return str(exponential)


def add_standard_to_dict(dict):
    for key, value in dict.items():
        if "Cost" in value:
            dict[key]["Standard Cost"] = convert_exponential_to_standard(value["Cost"])
        if "Evolutions" in value:
            for evolution, evolution_stats in value["Evolutions"].items():
                if evolution:
                    dict[key]["Evolutions"][evolution]["Standard Cost"] = convert_exponential_to_standard(
                        evolution_stats["Cost"])
    return dict


if __name__ == '__main__':
    # print(convert_standard_to_exponential("10.3 Vg"))
    # for i in range(0, 100):
    #     print(convert_exponential_to_standard(("3e" + str(i))))
    print(convert_standard_to_exponential("250 B"))
    # print(convert_exponential_to_standard("100 SP"))
    # print(convert_exponential_to_standard("100 T SP"))
    # print(convert_exponential_to_standard("0"))
    # print(convert_exponential_to_standard("1,000,000 SP"))
    # print(convert_exponential_to_standard("1e10"))
    # print(convert_exponential_to_standard("1e10"))
    # print(convert_exponential_to_standard("7e40"))
