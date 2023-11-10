import os
import time
import shutil

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def make_folder(name: str) -> None:
    if not os.path.isdir(name):
        os.mkdir(name)


def get_img(name: str, num_img: int) -> list:
    url = F'https://yandex.ru/images/search?text={name}'
    driver = webdriver.Edge()
    driver.get(url=url)
    driver.find_element(By.CSS_SELECTOR, 'a.Link').click()
    item = driver.find_element(By.CLASS_NAME, 'MMImage-Origin')
    items = item.get_attribute('src')
    links = [items]
    for i in range(num_img):
        try:
            time.sleep(0.5)
            driver.find_element(By.CLASS_NAME, 'MediaViewer-ButtonNext').click()
            img = driver.find_element(By.CLASS_NAME, 'MMImage-Origin')
            img_l = img.get_attribute('src')
        except:
            continue
    driver.quit()
    return links


def upload_img(name: str, links: list) -> None:
    make_folder(F'dataset/{name}')
    num_img = 0
    for img_l in links:
            while True:
                try:
                    time.sleep(3)
                    response = requests.get(img_l, verify=True)
                    if response.status_code == 200:
                        num_img += 1
                        with open(str(num_img).zfill(4) +'jpg', 'wb') as f_img:
                            f_img.write(response.content)
                            print('Excellent')
                            break
                except:
                    continue


def main() -> None:
    if os.path.isdir("dataset"):
        shutil.rmtree("dataset")
    
    num_img = 10

    name1 = 'polarbear'
    upload_img(name1, get_img(name1, num_img))

    name2 = 'brownbear' 
    upload_img(name2, get_img(name2, num_img))