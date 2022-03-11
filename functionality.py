import pydash as p
import requests
from bs4 import BeautifulSoup


def user_input():
    car = input("What car would you like results for?")
    return car


def page_nr(soup):
    page_num = soup.find_all("li", class_="e-page-number")[-1].text
    return page_num


def build_soup(make):
    url = f"https://www.autotrader.co.za/cars-for-sale/{p.strings.kebab_case(p.strings.lower_case(make))}"
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    return soup, url
