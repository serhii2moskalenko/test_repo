import json
import time
from bs4 import BeautifulSoup
import datetime
import csv
import asyncio
import aiohttp

phone_data = []
start_time = time.time()


async def get_page_data(session, page):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    url = f'https://www.ioutletstore.pt/categoria-produto/iphones/page/{page}/'
    async  with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')

        phone_items = soup.find('ul', class_='columns-4').find_all('li')
        for i in phone_items:
            try:
                phone_title = i.select('a')[1]['aria-label']
            except:
                phone_title = 'Нет названия'
            try:
                phone_price = i.select('bdi')[1].text.replace('€', '').replace(',', '.')
            except:
                phone_price = 'Нет цены'
            try:
                ram = phone_title.split(' / ', 1)[0].split()[-1].replace('GB', '')
            except:
                ram = 'Нет данных'
            try:
                color = phone_title.split(' / ', 1)[1]
            except:
                color = 'Неизвестен'
            try:
                phone_old_price = i.select('bdi')[0].text.replace('€', '').replace(',', '.')
            except:
                phone_old_price = 'Нет цены'
            try:
                phone_link = i.select('a')[1]['href']
            except:
                phone_link = 'Нет'
            try:
                img_link = i.find('img').get('data-lazy-src')
            except:
                img_link = 'Нет'

            phone_data.append(
                {
                    'phone_title': phone_title,
                    'ram': ram,
                    'color': color,
                    'phone_price': phone_price,
                    'phone_old_price': phone_old_price,
                    'phone_link': phone_link,
                    'img_link': img_link
                }
            )
        print(f'[INFO] Обработал страницу {page}')


async def gather_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    url = 'https://www.ioutletstore.pt/categoria-produto/iphones/'
    async  with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        all_pages = soup.find('nav', class_='woocommerce-pagination').find_all('li')
        pages_count = int(all_pages[-2].text)
        print(pages_count)
        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await  asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f'ioutletstore_phone_{cur_time}_async.json', 'w') as file:
        json.dump(phone_data, file, indent=4, ensure_ascii=False)

    with open(f'ioutletstore_phone_{cur_time}_async.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'phone_title',
                'ram',
                'color',
                'phone_price',
                'phone_old_price',
                'phone_link',
                'img_link'
            )
        )

    for phone in phone_data:
        with open(f'ioutletstore_phone_{cur_time}_async.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    phone['phone_title'],
                    phone['ram'],
                    phone['color'],
                    phone['phone_price'],
                    phone['phone_old_price'],
                    phone['phone_link'],
                    phone['img_link']
                )
            )

    finish_time = time.time() - start_time
    print(f'Затрачено: {finish_time}')


if __name__ == '__main__':
    main()
