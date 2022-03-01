import pydash as p


def car_brand(brand_name):
    return p.strings.kebab_case(p.strings.lower_case(brand_name))