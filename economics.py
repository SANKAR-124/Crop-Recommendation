import pandas as pd
import numpy as np



def calc_rev(crop_name):
    df=pd.read_json("crop_economics.json")
    crop=crop_name
    unit=df[crop_name]['unit']
    price_unit=df[crop_name]['price_per_unit']
    yield_acre=df[crop_name]['yield_per_acre']

    if unit=="quintal":
        price_per_kg=price_unit/100
        yield_kg=yield_acre*100
        revenue=int(price_per_kg*yield_kg)
        return {"crop":crop,"unit":unit, "revenue":revenue, "price_per_kg":price_per_kg, "yield_kg":yield_kg}
    elif unit=="kg":
        price_per_kg=price_unit
        yield_kg=yield_acre
        revenue=int(price_per_kg*yield_kg)
        return {"crop":crop,"unit":unit, "revenue":revenue, "price_per_kg":price_per_kg, "yield_kg":yield_kg}
    else:
        revenue=int(price_unit*yield_acre)
        return {"crop":crop,"unit":unit, "revenue":revenue, "price_unit":price_unit, "yield_acre":yield_acre}


    


# result=calc_rev(crop)
# print(result)