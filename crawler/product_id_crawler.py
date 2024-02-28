import requests
import time
import random
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': '8jWSuIDBb2NGVzr6hsUZXpkP1FRin7lY',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'limit': '40',
    'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
    'aggregations': '2',
    'trackity_id': '0206536e-01e1-7250-5ffc-44331ec1cec9',
    'category': '2549',
    'page': '1',
    'src': 'c2549',
    'urlKey': 'do-choi-me-be',
}

def parser_product_id(category, productId):
    d = dict()
    d['category'] = category
    d['product_id'] = productId
    return d

df_category = pd.read_csv('data/parent_category_data.csv')
print("Df Category: ", df_category)
cat = df_category.id.to_list()
print(cat)

product_id = []

for index, c in df_category.iterrows():
    print("Category", c)
    params['category'] = c.id
    params['src'] = c.src
    params['urlKey'] = c.urlKey
    for i in range(1, 11):
        params['page'] = i
        response = requests.get('https://tiki.vn/api/v2/products', headers=headers, params=params)
        try:
            response.raise_for_status()
            if response.status_code == 200:
                print('request success!!!')
                for record in response.json().get('data'):
                    id = record.get('id')
                    print(c.id, id)
                    print(parser_product_id(c.id, id))
                    product_id.append(parser_product_id(c.id, id))
        except requests.exceptions.HTTPError as err:
            print(err)
        except ValueError as err:
            print("Invalid JSON:", err)
            time.sleep(random.randrange(3, 10))

df = pd.DataFrame(product_id)
df.to_csv('data/product_id_data.csv', index=False)
