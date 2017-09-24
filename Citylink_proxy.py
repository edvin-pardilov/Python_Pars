# -*- coding: utf-8 -*
# ---------Подключение библиотек--------------------
import requests, time
from bs4 import BeautifulSoup
import MySQLdb
from random import choice
#-------------------------создание функции по нахождению данных о товарах----------
def get_product_info(url):
    r = requests.get(url, headers=headers,proxies=proxy)
    soup = BeautifulSoup(r.text, 'lxml')
    data['link'] = url #получаем линк
    data['name'] = soup.find('h1').text.strip() #получаем название
    s = soup.find('div',class_="price price_break")
    if s == None:
        data['price'] = -1
    else:
        data['price'] = soup.find('div',class_="price price_break").next.text.replace("руб", "")#получаем цену
    #data['price'] = data['price1'].soup.find('span')


#--------------------Подключение к базе данных--------------------
try:
    from db import conn
    sql = "INSERT INTO video_cards (href, name, price) values (\"%s\", \"%s\", %s)";#создаём строковую переменную с кодом запроса, символ %s означает, что на это место мы потом будем подставлять переменную

    conn.set_character_set('utf8')#устанавливае кодировку utf-8 иначе не робит
    data = dict()#для улучшения читабельности получает ссылку, словарь(именнованный массив)с инфой о товаре

    headers = {'User-agent': 'Mozilla/5.0'} #Выдаем себя за браузер
    url = 'https://www.citilink.ru/catalog/computers_and_notebooks/parts/videocards/?available=1&status=55395790&p=%s'
    j=0
    for url in [url % i for i in range(7,13)]:# создание цикла для постраничого парса
        if j % 3 == 0:
            proxies = open('C:\программа/proxies.txt').read().split('\n')
            proxy = {'http': 'http://' + choice(proxies)}# словарик с рандомным одним эелементом из файла proxies.txt
            print(proxy)
        r = requests.get(url, headers=headers,proxies=proxy)#Отправляем гет запрос регарду на получение информации с помощью реквеста
        soup = BeautifulSoup(r.text, 'lxml')#BeautifulSoup - это обертка для парсинга, он принимает два значения: 1)html код парсинга 2)тип парсера который следует использовать lxml - Python биндинг популярнойи и очень быстрой С библиотеки
        collect= soup.find_all('a', class_='link_gtm-js link_pageevents-js ddl_product_link')
        #product_links = (tag.get('href') for tag  in collect.find('a'))#Берем ссылки классов тегов, как бы обошли сам тег а и взли только его ссылки

        for link in collect:
            linka = link.get('href')
            print(linka)
            get_product_info(linka)#вызываем функцию
            try:
                if data['price'] == -1:
                    continue
                cur = conn.cursor()# создаём объект для работы с запросами
                o = int(data['price'].replace(" ", ""))# на сайте цена в виде строки мы приводим её к числовому типу и удаляем пробелы из неё
                cur.execute(sql, (data['link'], data['name'], o))# преобразуем строку, попутно подставляя в неё переменные в запрос
                conn.commit()#отправляем запрос в базу данных, для изменения данных
                time.sleep(20)
            except MySQLdb.Error as err:
                print("Query error: {}".format(err))#выводит ошибку если она есть
                conn.rollback()#отменяет изменения
    cur.close()#закрывает курсор
    conn.close()#закрывает коннект
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))
    conn.close()