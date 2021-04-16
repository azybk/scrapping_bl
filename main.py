import pandas as pd
import glob
from bs4 import BeautifulSoup
import requests
import json


def get_urls():
    res = requests.get('https://www.orami.co.id/shopping/category/fashion?page=2')
    soup = BeautifulSoup(res.text, 'html5lib')

    titles = soup.find_all('div',attrs={'class': 'jsx-3196085131 col-2 col-sm-2 col-md-2 col-lg-3 col-xl-4 bottom-m-md'})
    urls = []
    for title in titles:
        urls.append(title.find('a')['href'])

    return urls

def get_detail(url):
    res = requests.get('https://www.orami.co.id' + url)

    soup = BeautifulSoup(res.text, 'html5lib')
    item_title = soup.find('h1', attrs={'class': 'prod-detail-title mb-8 loading'}).text.strip()
    price = soup.find('div', attrs={'class': 'w-100 d-flex align-items-center'}).text.strip().\
                        replace('Stok Habis','').replace('Rp ','')
    description = soup.find('div', attrs={'class': 'prod-detail-description'}).text.strip().replace('\n',' ')

    dict_data = {
        'title': item_title,
        'price': price,
        'description': description
    }

    with open('./results/{}.json'.format(url.replace('/','')), 'w') as outfile:
        json.dump(dict_data, outfile)


def create_csv():
    files = sorted(glob.glob('./results/*.json'))

    datas =[]
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)
    print('csv generated...')


def run():
    total_urls = get_urls()

    i = 0
    for all_urls in total_urls:
        print(all_urls)
        i+=1

    with open('all_urls.json', 'w') as outfile:
        json.dump(total_urls, outfile)

    with open('all_urls.json') as json_file:
        data = json.load(json_file)

    for data_url in data:
        print(f'get detail...{data_url}')
        get_detail(data_url)

    # get_detail('shopping/product/takoyakids-yuki-set-atlantic-blue-5-6-year')
    create_csv()


if __name__ == '__main__':
    run()
