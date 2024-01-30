import requests
from bs4 import BeautifulSoup
import datetime
import time
import sql_module as sm

folder = './parser4510/'

#sm.sm_test()
#sm.create_base(way1=folder)

def parser(url:str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, 'lxml')
    products = soup.find_all('div', class_='p__bottom')
    
    for product in products:
        name1 = product.find('a', class_='p__title').get('title')
        link1 = product.find('a').get('href')
        link1 = 'https://tamaris.ru' + link1
        price1 = product.find('div', class_='p__price').text
        price1 = price1.strip() #уд. пустоту в начале и в конце строки (первая цена окажется в начале)
        price1 = price1[0:15]   #берём срез 16 символов от начала (первая цена уместится 100%)
        price1 = price1.replace('р.', '')#удаляем надпись "рублей"
        price1 = price1.replace(' ', '')#удаляем ненужные пробелы
        price1 = int(price1)#конвертируем цену из текста в число, тип переменной теперь int
        print(f'{name1} {price1} {link1}')
 
    

def make_url_list(url):#начинаем с начального адреса и проверяем доступность страниц
    url_list = open('./parser4510/url_list.txt', '+w')
    url_list.write(url+'\n')
    #?PAGEN_1=2,?PAGEN_1=3... 
    
    for i in range(2,23):    
        urlx = url + '?PAGEN_1=' + str(i)
        if requests.get(urlx).status_code == 200:
            print(urlx + '\n')
            url_list.write(urlx+'\n')

    url_list.close
    
    #with open('./parser4510/url_list.txt') as url_list:
    #    l1 = url_list.readline()
    #    print(l1)


if __name__ == "__main__":
    #make_url_list(url="https://tamaris.ru/catalog/obuv/")
    parser(url="https://tamaris.ru/catalog/obuv/")
    #pass