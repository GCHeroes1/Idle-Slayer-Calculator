from Conversion import convert_standard_to_exponential

evolution_discounts = {
    "Cheap Darkness": {
        "Cost": convert_standard_to_exponential("5 Qa"),
        "Benefit": float(0.5)
    },
    "Embrace The Fear": {
        "Cost": convert_standard_to_exponential("10 Oc"),
        "Benefit": float(0.25)
    },
    "Generations": {
        "Cost": convert_standard_to_exponential("10 Nd"),
        "Benefit": float(0.001)
    }
}
