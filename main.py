import requests
import pandas
from functionality import build_soup, user_input, page_nr
import numpy as np
import pydash as p
from bs4 import BeautifulSoup

make = user_input()
soup, url = build_soup(make)
brand_param = p.strings.substr_right(url, "cars-for-sale/")
brand_param = p.strings.to_upper(brand_param).replace("-"," ")

l = []


for page in range(1, int(page_nr(soup)) + 1):
    new_url = url + f"?pagenumber={page}"
    r = requests.get(new_url)
    c = r.content
    new_soup = BeautifulSoup(c, "html.parser")

    all = new_soup.find_all("div", {"class": "b-result-tile"})

    print(page)

    for item in all:
        d = {}
        text = p.strings.to_upper(item.find("span", {"class": "e-title"}).text)
        d["Brand"] = brand_param
        d["Model"] = p.strings.substr_right((text), d["Brand"])
        d["New/Used"] = item.find("span", {"class": "e-type"}).text
        d["Price"] = item.find("span", {"class": "e-price"}).text.replace(" ", "").replace("R", "")
        d["Monthly Repayment"] = (item.find("span", {"class": "e-estimated-payment" if (
            item.find("span", {"class": "e-estimated-payment"})) else "e-price"}).text.replace(" ", "").replace("\n",
                                                                                                                ""))

        if d["Monthly Repayment"] == d["Price"]:
            pass
        else:
            d["Monthly Repayment"] = d["Monthly Repayment"].replace("R", "").replace("p/m", "")
            d["Monthly Repayment"] = int(d["Monthly Repayment"])

        for fgroup in item.find_all("span", {"class": "e-icons"}):
            d["year"] = fgroup.text[0:4]

            for details in fgroup.find_all("span"):
                img = details.find("img")
                transmission_string = "gearbox"
                mileage_string = "mileage"

                if transmission_string in img["src"]:
                    d["Transmission"] = details.text

                if mileage_string in img["src"]:
                    d["Mileage"] = details.text.replace("km","")



        l.append(d)

df = pandas.DataFrame(l)
df["Model"].replace('', np.nan, inplace=True)
df.dropna(subset=["Model"], inplace=True)
df.to_excel("Cars.xlsx")

print(df)




























