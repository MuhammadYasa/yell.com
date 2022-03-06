import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
import openpyxl


base_url = 'https://www.yell.com/'
url = 'https://www.yell.com/ucs/UcsSearchAction.do?'

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
}

def get_total_pages(searches):
    params = {
        'keywords' : 'Italian Reataurants',
        'location' : 'Houghton Le Spring',
        'scrambleSeed' : '1581452655',
        'key' : searches,
        'pg' : 1,
    }

    res = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')

    pages = []
    headers_contents = soup.find('div', 'col-sm-14 col-md-16 col-lg-14 text-center').find_all('a')
    for i in headers_contents:
        pages.append(int(i.text))

    print(headers_contents)
    total_pages = max(pages)
    print(total_pages)
    return total_pages

def get_all_item(searches, pages):
    restaurant_list = []
    params = {
        'keywords': 'Italian Reataurants',
        'location': 'Houghton Le Spring',
        'scrambleSeed': '1581452655',
        'key': searches,
        'pg': pages,
    }
    res = requests.get(url, params=params, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find('div', {'class' : 'row results--row results--capsuleList'})
    contents = results.find_all('div', {'class':'row businessCapsule--mainRow'})

    for content in contents:
        title = content.find('h2', 'businessCapsule--name text-h2').text
        classification = content.find('span', 'businessCapsule--classification').text
        link_web = base_url + content.find('div', 'businessCapsule--titSpons').find('a')['href']

        telephone = content.find('span', 'business--telephoneNumber')
        if telephone is not None:
            telephone = telephone.text
        else:
            telephone = 'Telephone is not available'

        final_data = {
            'title': title,
            'classification': classification,
            'telephone': telephone,
            'link web': link_web,
        }

        restaurant_list.append(final_data)

    return restaurant_list

def output(searches, final_result):
    # export to csv or excel
    df = pd.DataFrame(final_result)
    df.to_csv(f'{searches}.csv', index=False)
    df.to_excel(f'{searches}.xlsx', index=False)

def main(searches):
    final_result = []

    total_pages = get_total_pages(searches)
    for page in range (total_pages):
        page += 1
        print(f'Scraping halaman ke : {page}')
        products = get_all_item(searches, page)
        final_result += products

    # the processing data
    total_data = len(final_result)
    print(f'total page after scraping {format(total_data)}')

    # export to csv
    output(searches, final_result)

if __name__ == '__main__':
    searches = ('restaurants')
    main(searches)



# data created
print('Data Created Succes')