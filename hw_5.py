"""
Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from time import time

option = Options()
option.add_argument('--disable-notifications')  # отключаем уведомления чтобы не мешали.

# s = Service('chromedriver.exe')
driver = webdriver.Chrome(options=option)
driver.get('https://www.mvideo.ru/')
action = ActionChains(driver)

action.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN)
action.perform()


trends = Wait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@class="tab-button ng-star-inserted"]')
        )
    )

action.click(trends).perform()

goods = driver.find_elements(By.XPATH, '//a[@class="ng-star-inserted"]/text()')
print(goods)
driver.close()

"""
selenium.common.exceptions.WebDriverException: Message: target frame detached
"""
