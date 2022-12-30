import requests
from bs4 import BeautifulSoup

URL = "https://nitecore.ua/ua/category/nalobnie-fonari/"

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


def get_html(url):
    req = requests.get(url=url, headers=HEADERS)
    return req


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="col-md-3 col-sm-6 col-6 product-card-wrapper")
    news = []
    for item in items:
        card = {
            'title': item.find('div', class_='product-title').find('a').string,
            'link': item.find('div', class_="product-title").find('a').get('href'),
            'price': item.find('div', class_="price").find('span').string
        }
        news.append(card)
    return news
    # pprint(news)

# html = get_html(URL)
# get_data(html.text)


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        for i in range(1, 2):
            html = get_html(f"{URL}page/{i}/")
            current_page = get_data(html.text)
            news.extend(current_page)
        return news
    else:
        raise Exception("Bad request!")
