import requests
from bs4 import BeautifulSoup
import csv

def parser(url:str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, "lxml")
    #products = soup.find_all("div",class_="p__bottom")
    products = soup.find_all(class_="p__title")
    print (f'найдено:{len(products)}')
    for product in products:
        name = product.get("title")
        #price = product.find 
        
        print(name, price)

def create_csv():
    pass

def write_csv():
    pass

if __name__ == "__main__":
    parser(url="https://tamaris.ru/catalog/obuv/")