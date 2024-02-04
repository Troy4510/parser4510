import requests
from bs4 import BeautifulSoup
import datetime
import time
import os.path
import sql_module as sm

main_folder = './parser4510/'

#временная логика
pages_count = 22
makelinks = False
make_sql_base = True
multiparce_flag = True

def parser_1page(url):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, 'lxml')
    products = soup.find_all('div', class_='p__bottom')
    print(f'products found: {len(products)}')
    
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
        print(f'[add to sql_base] {name1} {price1}')
        #проверка наличия в базе и внесение записи/изменение статуса
        sm.check_record(main_folder, name1, link1, price1)
            
    

def make_url_list(url):#начинаем с начального адреса и проверяем доступность страниц
    url_list = open(f'{main_folder}url_list.txt', '+w')
    #url_list.write(url+'\n')
    #?PAGEN_1=2,?PAGEN_1=3... 
    
    for i in range(1,pages_count+1):    
        urlx = url + '?PAGEN_1=' + str(i)
        if requests.get(urlx).status_code == 200:
            print(urlx)
            url_list.write(urlx+'\n')

    url_list.close


def multiparce():
    print('[multiparce]')
    work_url_list = main_folder + 'url_list.txt'
    workfile = open(work_url_list, '+r')
    
    for i in range(pages_count):
        link1 = workfile.readline()
        print('/n[parse] ' + link1)
        parser_1page(link1)
        
    workfile.close()


if __name__ == "__main__":
    print('[RUN MAIN]')
    #if make_sql_base == True: sm.check_base(db_folder=main_folder)
    #if makelinks == True: make_url_list(url="https://tamaris.ru/catalog/obuv/")
    #if os.path.exists(main_folder + 'url_list.txt') and multiparce_flag == True: multiparce()
    #sm.erase_sverka(main_folder)
    #print(sm.counter(main_folder))
    #print(sm.read_record(main_folder, 1))
    #ans = sm.check_record(main_folder, 'Туфли лодочки кожаные', 'https://tamaris.ru/catalog/obuv/tufli_1/tufli_zakrytye/tufli-lodochki-kozhanye-1-22434-41-418/', 9995)
    #print(ans)