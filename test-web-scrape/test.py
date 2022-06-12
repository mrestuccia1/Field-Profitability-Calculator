#!/usr/bin/env python3

import json
with open('states.json') as f:
    data = json.load(f)

for state in data['states']:
    print (state['name'], state['abbreviation'])


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://en.wikipedia.org/wiki/Table_(information)'
requests.get(url)
page = requests.get(url)

soup = BeautifulSoup(page.text, 'lxml')


table_data = soup.find('table', class_ = 'wikitable')

headers = []
for i in table_data.find_all('th'):
    title = i.text
    headers.append(title)

df = pd.DataFrame(columns = headers)

for j in table_data.find_all('tr')[1:]:
        row_data = j.find_all('td')
        name = row_data[0]
        last = row_data[1]
        print (name.text.strip(), last.text.strip())

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

site = 'https://ahdb.org.uk/cereals-oilseeds-markets'

wd = webdriver.Chrome('chromedriver',options=options)
wd.get(site)

