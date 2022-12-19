'''
Online shop site parser. Data saving in a data base SQLite and 'File'.csv
'''
import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import sqlalchemy as db
import lxml

CSV = 'smartfony_test.csv'
URL = 'https://dm.kh.ua/532-smartfony/'    # page address from where parsing starts

'''
'accept' -indicates which types of content the client can understand;
'user-agent' - this is a string with characteristics by which the server and network nodes
can determine the type of application, operating system, manufacturer
and/or user agent version

'''
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
}


def get_html(url, params=''):
    '''
    Accesses the page via query and gets content as HTML
    '''
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    '''
    Get an Item Card from the Received Page with lxml parser
    '''
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='product-container')
    cards = []

    for item in items:
        cards.append(
            {
                'model': item.find('a', class_='product-name').get_text(strip=True),
                'brand': item.find('meta', itemprop="brand").get('content'),
                'link_product': item.find('a', class_='product-name').get('href'),
                'price': item.find('span', class_='price product-price').get_text(strip=True).replace(' ', '').replace(
                    'грн', ''),
                'card_img': item.find(class_='replace-2x img-responsive lazy img_0 img_1e').get('data-original'),
                'availability_status': item.find('p', id='availability_statut').find('span').get_text(strip=True)
            }
        )
    return cards


def to_csv(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['model', 'brand', 'link_to_product', 'price', 'card_img', 'availability'])
        for item in items:
            writer.writerow([item['model'], item['brand'], item['link_product'], item['price'], item['card_img'],
                             item['availability_status']])


def to_base(items):
    engine = db.create_engine('sqlite:///s2b_test.db')
    connection = engine.connect()
    metadata = db.MetaData()

    products = db.Table('smartphones', metadata,
                        db.Column('product_id', db.Integer, primary_key=True),
                        db.Column('model', db.Text),
                        db.Column('brand', db.Text ),
                        db.Column('link_product', db.Text),
                        db.Column('price', db.Integer),
                        db.Column('card_img', db.Text),
                        db.Column('availability_status', db.Text)
                        )

    metadata.create_all(engine)

    insertion = products.insert().values(items)

    connection.execute(insertion)


def parser():
    '''
    Processes and sequentially runs the entire code
    '''
    PAGENATION = int(input("Укажите количество страниц для обработки ").strip())  # number of pages for parsing
    html = get_html(URL)
    if html.status_code == 200:  # check the availability of the requested page
        cards_all = []
        for page in range(1, PAGENATION + 1):
            sleep(3)  # timeout between page processing
            print(f'Обработка страницы: {page}')
            html = get_html(f'{URL}#/page-{page}/', params={'page': page})
            cards_all.extend(get_content(html.text))    # get the content we need from the text obtained from HTML
            to_csv(cards_all, CSV)
            to_base(cards_all)
        print('THE END')
    else:
        print('Error')  # if the page is not available


parser()
