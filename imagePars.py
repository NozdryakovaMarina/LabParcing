import os
import cv2 
from time import sleep 
from selenium import wevdriver

from bs4 import BeautifulSoup
import requests

URL = "https://yandex.ru/images/search/?from=tabbar&text=bears"
html_page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
html_page.encoding = 'utf-8'
src = html_page.text
soup = BeautifulSoup(src, "lxml")
names = soup.find_all('img', {'class': ['serp-item__thumb justifier__thumb']})

if not os.path.isdir("brown_bear"):
    os.mkdir("brown_bear")

for item in names:
    print(item.text)

all_links = soup.find_all('a', 'href')
for item in all_links:
    link =item.get('href')
    print(link)


parent_blocks = soup.find_all('div',{'class': ['serp-item serp-item_type_search serp-item_group_search serp-item_pos_1 justifier__item i-bem serp-item_js_inited justifier__item_first justifier__item_last']})
for parent_block in parent_blocks:
    name = parent_block.find('div', {'class': ['serp-item_meta']})
    print(name.text)
    link = parent_block.find('a')
    print(link.get('href'))

#print(soup.text)