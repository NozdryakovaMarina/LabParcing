import os
import time
import shutil
from typing import List

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def make_folder(name: str) -> None:
    """
    The function creates a directory if it does not exist
    """
    if not os.path.isdir(name):
        os.mkdir(name)


def get_img(name: str, num_img: int) -> List[str]:
    """
    The function opens a page in the browser using a link to search for a 
    given class of images {name: str}, using the element code, scroll through a 
    given number of images {num_img: int} and get links to them, saving them 
    sequentially in the list
    """
    url = F'https://yandex.ru/images/search?text={name}'
    driver = webdriver.Edge()
    driver.get(url=url)
    driver.find_element(By.CSS_SELECTOR, 'a.Link').click()
    links = []
    for i in range(num_img):
        try:
            time.sleep(0.05)
            driver.find_element(By.CLASS_NAME, 'MediaViewer-ButtonNext').click()
            img = driver.find_element(By.CLASS_NAME, 'MMImage-Origin')
            img_l = img.get_attribute('src')
            links.append(img_l)
        except:
            continue
    driver.quit()
    return links


def upload_img(name: str, links: List[str]) -> None:
    """
    The function creates a subdirectory in the directory with the name of the class 
    {name: str}, runs through the list {links: List[str]}, loads images and saves 
    them in the specified subdirectory
    """
    make_folder(f"dataset/{name}")
    num_img = 0
    for img_l in links:
            while True:
                try:
                    time.sleep(1)
                    response = requests.get(img_l, verify=True)
                    if response.status_code == 200:
                        with open(F'dataset/{name}/{str(num_img).zfill(4)}' + '.jpg', 'wb') as f_img:
                            f_img.write(response.content)
                            print('Excellent')
                        num_img += 1
                        break
                except:
                    continue


def main() -> None:

    if os.path.isdir("dataset"):
        shutil.rmtree("dataset")

    make_folder('dataset')
    name1 = 'polar_bear'
    name2 = 'brown_bear'
    num_img = 1100

    upload_img(name1, get_img(name1, num_img))
    time.sleep(5)
    upload_img(name2, get_img(name2, num_img))