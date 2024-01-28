import requests
from bs4 import BeautifulSoup


def parser(url:str):
    res = requests.get(url=url)
    if res.status_code == 200:
        print('страница доступна')
    soup = BeautifulSoup(res.text, 'lxml')
    #products = soup.find_all('div', class_='p__bottom')
    products_names = soup.find_all('a', class_='p__title')
    products_prices = soup.find_all('div',class_='p__price p__price--old')
    
    #print (f'найдено products:{len(products)}')
    print (f'найдено names:{len(products_names)}')
    print (f'найдено prices:{len(products_prices)}')
    
    for i in range(len(products_names)):
         n1 = products_names[i].text
         n1 = n1.strip()
         p1 = products_prices[i].text
         p1 = p1.strip()
         p1 = p1.replace(' р.', '')
         p1 = p1.replace(' ', '')
         p1 = int(p1)
         print(f'№{i+1}. {n1} {p1} р.')
         
    #for price in products_prices:
        #price = price.text
        #price = price.strip() #уд пробелы в начале и в конце
        #или price = price.replace(' ', '')
        #print(price)

    #for name in products_names:
    #    print (name.text)
        
    #for product in products:
    #    print(product)
       

if __name__ == "__main__":
    parser(url="https://tamaris.ru/catalog/obuv/")