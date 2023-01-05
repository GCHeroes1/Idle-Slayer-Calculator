standardNotation = ["M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "De", "Ud", "Dd", "Td", "Qt", "Qd", "St",
                    "Sd", "Od", "Nd", "Vg", "Uv", "Dv", "Tv", "Qav", "Qiv", "Sxv", "Spv", "Ocv"]
exponentials = [float("1e6"), float("1e9"), float("1e12"), float("1e15"), float("1e18"), float("1e21"), float("1e24"),
                float("1e27"), float("1e30"), float("1e33"), float("1e36"), float("1e39"), float("1e42"), float("1e45"),
                float("1e48"), float("1e51"), float("1e54"), float("1e57"), float("1e60"), float("1e63"), float("1e66"),
                float("1e69"), float("1e72"), float("1e75"), float("1e78"), float("1e81"), float("1e84"), float("1e87")]


def convert_standard_to_exponential(coinsRecord):
    abbreviation = coinsRecord[-2:]
    coins = float(coinsRecord[:-3])
    index = standardNotation.index(abbreviation)

    return coins * exponentials[index]


if __name__ == '__main__':
    print(convert_standard_to_exponential("10.3 Vg"))
