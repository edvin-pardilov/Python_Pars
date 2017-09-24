# -*- coding: utf-8 -*
# ---------Подключение библиотек--------------------
import requests, time
from bs4 import BeautifulSoup
import MySQLdb
from random import choice
#-------------------------создание функции по нахождению данных о товарах----------
def get_product_info(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    data['link'] = url #получаем линк
    data['name'] = soup.find('h1').text.strip() #получаем название
    data['price'] = soup.find('span',class_="js__actualPrice").next_element.next_element.text#получаем цену
    #data['price'] = data['price1'].soup.find('span')
#--------------------Подключение к базе данных--------------------
try:
    conn = MySQLdb.connect(host="edvin9kc.beget.tech", user="edvin9kc_edvin",
                           passwd="iopl87jkl", db="edvin9kc_edvin")#подключаемся к базе
    sql = "INSERT INTO video_cards (href, name, price) values (\"%s\", \"%s\", %s)";#создаём строковую переменную с кодом запроса, символ %s означает, что на это место мы потом будем подставлять переменную

    conn.set_character_set('utf8')#устанавливае кодировку utf-8 иначе не робит
    data = dict()#для улучшения читабельности получает ссылку, словарь(именнованный массив)с инфой о товаре
    headers = {'User-agent': 'Mozilla/5.0'} #Выдаем себя за браузер
    url = 'https://www.onlinetrade.ru/catalogue/videokarty-c338/?page=%s'
    proxy = None


    for url in [url % i for i in range(1,22)]:# создание цикла для постраничого парса
        proxies = open('C:\программа/proxies.txt').read().split('\n')
        proxy = {'http': 'http://' + choice(proxies)}# словарик с рандомным одним эелементом из файла proxies.txt
        print(proxy)
        r = requests.get(url, headers=headers, proxies=proxy)#Отправляем гет запрос регарду на получение информации с помощью реквеста
        soup = BeautifulSoup(r.text, 'lxml')#BeautifulSoup - это обертка для парсинга, он принимает два значения: 1)html код парсинга 2)тип парсера который следует использовать lxml - Python биндинг популярнойи и очень быстрой С библиотеки
        collect= soup.find_all('div', class_='catalog__displayedItem__name')
        #product_links = (tag.get('href') for tag  in collect.find('a'))#Берем ссылки классов тегов, как бы обошли сам тег а и взли только его ссылки

        for link in collect:
            linka = link.find('a').get('href')
            print('https://www.onlinetrade.ru'+linka)
            get_product_info('https://www.onlinetrade.ru'+linka)#вызываем функцию
            try:
                cur = conn.cursor()# создаём объект для работы с запросами
                o = int(data['price'].replace(" ", ""))# на сайте цена в виде строки мы приводим её к числовому типу и удаляем пробелы из неё
                cur.execute(sql, (data['link'], data['name'], o))# преобразуем строку, попутно подставляя в неё переменные в запрос
                conn.commit()#отправляем запрос в базу данных, для изменения данных
                time.sleep(1)
            except MySQLdb.Error as err:
                print("Query error: {}".format(err))#выводит ошибку если она есть
                conn.rollback()#отменяет изменения
    cur.close()#закрывает курсор
    conn.close()#закрывает коннект
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))
    conn.close()