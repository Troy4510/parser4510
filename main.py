import requests
from bs4 import BeautifulSoup
import datetime


def parser(url:str):
    res = requests.get(url=url)
    if res.status_code == 200:
        print('страница доступна')
    soup = BeautifulSoup(res.text, 'lxml')
 
    products = soup.find_all('div', class_='p__bottom')
    
    for product in products:
        name1 = product.find('a', class_='p__title').get('title')
        price1 = product.find('div', class_='p__price').text
        price1 = price1.strip() #уд. пустоту в начале и в конце строки (первая цена окажется в начале)
        price1 = price1[0:15]   #берём срез 16 символов от начала (первая цена уместится 100%)
        price1 = price1.replace('р.', '')#удаляем надпись "рублей"
        price1 = price1.replace(' ', '')#удаляем ненужные пробелы
        price1 = int(price1)#конвертируем цену из текста в число, тип переменной теперь int
        
        print(f'{name1} - {price1} р.')
 
    

def make_url_list(url):#начинаем с начального адреса и проверяем доступность страниц
    url_list = open('./parser4510/url_list.txt', '+w')
    #?PAGEN_1=2,3,4...
    try:
        for i in range(5):
            url_list.write(url+'\n')
    finally:
        url_list.close
    
    #with open('./parser4510/url_list.txt') as url_list:
    #    l1 = url_list.readline()
    #    print(l1)


if __name__ == "__main__":
    #make_url_list(url="https://tamaris.ru/catalog/obuv/")
    parser(url="https://tamaris.ru/catalog/obuv/")
    