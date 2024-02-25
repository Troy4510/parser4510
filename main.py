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
parse_today = False

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
    print(f'{datetime.datetime.now()} [MAIN: make_url_list init]')

    for i in range(1,pages_count+1): 
        urlx = url + '?PAGEN_1=' + str(i)
        
        if requests.get(urlx).status_code == 200:
            print(f'[check page] {urlx}')
            url_list.write(urlx+'\n')
            
    url_list.close
    print(f'{datetime.datetime.now()} [MAIN: make_url_list complete]')


def multiparce():
    print(f'{datetime.datetime.now()} [MAIN: multiparce start]')
    work_url_list = main_folder + 'url_list.txt'
    workfile = open(work_url_list, '+r')
    
    for i in range(pages_count):
        link1 = workfile.readline()
        print('/n[parse] ' + link1)
        parser_1page(link1)#постраничный запуск парсера (построчно из url-файла)
        
    workfile.close()
    print(f'{datetime.datetime.now()} [MAIN: multiparce end]')

    

if __name__ == "__main__":
    print(f'{datetime.datetime.now()} [RUN MAIN]')
    
    #проверяет наличие базы и если её нет - создаёт
    if os.path.exists(main_folder + 'sql_base.db') == False and check_sql_base == True: 
        sm.check_base(db_folder=main_folder)
        print(f'{datetime.datetime.now()} [MAIN: sql_base created]')
    
    #создаёт url-список для проверки в виде файла
    if os.path.exists(main_folder + 'url_list.txt') == False and makelinks == True: 
        make_url_list(url="https://tamaris.ru/catalog/obuv/")
        print(f'{datetime.datetime.now()} [MAIN: url_list created]')
    
    #запускает первую процедуру парсинга если база пустая
    if sm.counter(main_folder) == None and zero_launch_check == True:
        print(f'{datetime.datetime.now()} [MAIN: zero_start init]')
        multiparce()
        #и делает первую запись в tStat
        date_upd = datetime.datetime.now()
        vsego = sm.counter(main_folder)
        insert_product = sm.added_products
        delete_product = sm.deleted_products
        sm.write_stat(main_folder, date_upd, vsego, insert_product, delete_product)
        sm.added_products = 0
        sm.deleted_products = 0
        print(f'{datetime.datetime.now()} [MAIN: zero_start complete]')
    
    print(f'{datetime.datetime.now()} [MAIN: check complete]')
    
    #основной цикл
    time_now = time.time()
    time_next = time_now + 100
    print(f'{datetime.datetime.now()} [MAIN: start core]')
    
    while True:
        if time.time() >= time_next:            #когда сработал будильник
            sm.added_products = 0               #обнуляется счётчик добавленных
            sm.deleted_products = 0             #обнуляется счётчик удалённых
            sm.erase_sverka(main_folder)        #все записи базы меняют статус на 'need_check'
            multiparce()                        #запускается парсер, счётчики и статусы проверенных на 'ok'
            sm.erase_unchecked(main_folder)     #удаляются товары которых нет на сайте (статус 'need_check' не сменился на 'ok')
            date_upd = datetime.datetime.now().strftime('%d.%m.%y/%H:%M')  #дата для внесения в таблицу статистики
            vsego = sm.counter(main_folder)     #количество записей для таблицы статистики
            insert_product = sm.added_products  #количество добавленных
            delete_product = sm.deleted_products    #количество удалённых
            sm.write_stat(main_folder, date_upd, vsego, insert_product, delete_product) #запись в таблицу статистики
            time_now = time.time()              #сбрасывается отсчёт времени
            time_next = time_now + 86400        #ставится будильник на сутки вперед
        else:                                   #иначе раз в полчаса и делать запись об ожидании и дальше спать
            print(f'{datetime.datetime.now()} [MAIN: core wait ok...]')
            time.sleep(1800)
    #не забыть! дистанционный запуск на сервере всегда делать через nohup чтоб работало в фоне и оставались логи консоли
    
    
    #всякие пробы))) 
    #прим.: час - 3600 сек, сутки - 86400 сек
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