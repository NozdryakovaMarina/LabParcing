import os
import time
import shutil

import requests
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By


def  make_folders(name: list) -> None:
    if not os.path.isdir('dataset'):
        os.mkdir('dataset')
        
    os.chdir('dataset')
    if os.isdir(name[0]) and os.isdir(name[1]):
        shutil.rmtree(name[0])
        shutil.rmtree(name[1])
    os.mkdir(name[0])
    os.mkdir(name[1])


def get_link(request):
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    URL = f"https://yandex.ru/images/search?text={request}"
    driver.get(URL=URL)
    driver.maximize_window()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, 'div.serp-item__preview a.serp-item__link').click()

    with open(f"urls_{request}.txt", 'w') as file:
        for i in range(0, 1500):
            try:
                time.sleep(0.05)
                link = driver.find_element(By.CSS_SELECTOR, "a.Button2_view_action").get_attribute("href")
                file.write(link + '\n')
                driver.find_element(By.CSS_SELECTOR, "div.CircleButton:nth-child(4)").click()
            except:
                continue
    driver.quit()


def get_image(name: str) -> None:
    os.chdir(name)

    count = 0
    with open(f"urls_{name}.txt", "r") as file:
        for line in file:
            try:
                url = line.strip()
                time.sleep(2)
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    count+=1
                    with open(f"dataset/{name}/{str(count).zfill(4)}.jpg", "wb") as image_file:
                        shutil.copyfileobj(response.raw, image_file)
                else:
                    continue
            except:
                continue
    print(f'{count} Succecs!')
    

def main() -> None:
    type1 = 'polarbear'
    type2 = 'brownbear'
    make_folders((type1, type2))
    get_image(type1)
    get_image(type2)