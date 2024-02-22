import requests
from bs4 import BeautifulSoup
import datetime
import time
import os.path
import sql_module as sm

main_folder = './parser4510/'

#логика и параметры
pages_count = 22
makelinks = True
check_sql_base = True
zero_launch_check = True

def parser_1page(url): #парсит одну страницу по ссылке и заносит товары в базу
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
    print('[MAIN: make_url_list init]')
    #url_list.write(url+'\n')
    #?PAGEN_1=2,?PAGEN_1=3... 
    for i in range(1,pages_count+1): 
        urlx = url + '?PAGEN_1=' + str(i)
        
        if requests.get(urlx).status_code == 200:
            print(f'[check page] {urlx}')
            url_list.write(urlx+'\n')
            
    url_list.close
    print('[MAIN: make_url_list complete]')


def multiparce():
    print('[MAIN: multiparce start]')
    work_url_list = main_folder + 'url_list.txt'
    workfile = open(work_url_list, '+r')
    
    for i in range(pages_count):
        link1 = workfile.readline()
        print('/n[parse] ' + link1)
        parser_1page(link1)#постраничный запуск парсера (построчно из url-файла)
        
    workfile.close()
    print('[MAIN: multiparce end]')

    

if __name__ == "__main__":
    print('[RUN MAIN]')
    
    #проверяет наличие базы и если её нет - создаёт
    if os.path.exists(main_folder + 'sql_base.db') == False and check_sql_base == True: 
        sm.check_base(db_folder=main_folder)
        print('[MAIN: sql_base created]')
    
    #создаёт url-список для проверки в виде файла
    if os.path.exists(main_folder + 'url_list.txt') == False and makelinks == True: 
        make_url_list(url="https://tamaris.ru/catalog/obuv/")
        print('[MAIN: url_list created]')
    
    #запускает первую процедуру парсинга если база пустая
    if sm.counter(main_folder) == None and zero_launch_check == True:
        print('[MAIN: zero_start init]')
        multiparce()
        #и делает первую запись в tStat
        date_upd = datetime.datetime.now()
        vsego = sm.counter(main_folder)
        insert_product = sm.added_products
        delete_product = sm.deleted_products
        sm.write_stat(main_folder, date_upd, vsego, insert_product, delete_product)
        sm.added_products = 0
        sm.deleted_products = 0
        print('[MAIN: zero_start complete]')
    
    print('[MAIN: check complete]')
    #while True:
    
    
    
    #всякие пробы))) прим.: час - 3600 сек, сутки - 86400 сек
    #print(os.path.exists(main_folder + 'sql_base.db'))    
    #sm.erase_sverka(main_folder)
    #print(sm.counter(main_folder))
    #print(sm.read_record(main_folder, 1))
    #ans = sm.check_record(main_folder, 'Туфли лодочки кожаные', 'https://tamaris.ru/catalog/obuv/tufli_1/tufli_zakrytye/tufli-lodochki-kozhanye-1-22434-41-418/', 9995)
    #print(ans)
    #sm.added_products +=1
    #print(sm.added_products)
    #sm.test()
    #print(sm.added_products)
    #print(sm.erase_unchecked(main_folder))
    #print('[MAIN END]')
    #дата апдейта, общее количество на конец апдейта, добавлено, удалено