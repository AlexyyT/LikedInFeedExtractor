from utilities import *

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs
import pandas as pd


if __name__ == '__main__':
    driver_path = "C:\\Users\\ATOU\\Downloads\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)

    wait = WebDriverWait(driver, 20)

    # Go to linkedin and login
    driver.get('https://www.linkedin.com/login')

    linkedin_connexion(driver, "toulou26@hotmail.fr", "AxyTmt26")
    time.sleep(5)

    driver.get('https://www.linkedin.com/company/hippopotamus-fr/posts/?feedView=all')
    time.sleep(5)

    scroll_down_feed(driver, 1.5)
    print('Scroll OK')
    time.sleep(5)

    # SCROLL_PAUSE_TIME = 1.5
    #
    # # Get scroll height
    # last_height = get_height(driver)
    #
    # while True:
    #     scroll_down(driver)
    #
    #     time.sleep(SCROLL_PAUSE_TIME)
    #
    #     new_height = get_height(driver)
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    # posts_page = driver.page_source
    # linkedin_soup = bs(posts_page, "html")

    linkedin_soup = get_soup(driver)

    body = driver.find_element(By.CLASS_NAME, 'render-mode-VANILLA.nav-v2.ember-application.icons-loaded.boot-complete')
    executor(driver, body)

    time.sleep(5)

    try:
        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[contains(normalize-space(@class),'t-black--light social-details-social-counts__count-value t-12 hoverable-link-text')]")))
        showmore_link.click()

    except ElementClickInterceptedException:
        print("Trying to click on the button again")
        driver.execute_script("arguments[0].click()", showmore_link)

    # btn = driver.find_element(By.XPATH, "//button[contains(normalize-space(@class),'t-black--light social-details-social-counts__count-value t-12 hoverable-link-text')]")
    # btn.click()
    # time.sleep(5)

    # classe_name='t-black--light social-details-social-counts__count-value t-12 hoverable-link-text'
    # btn_soup = linkedin_soup.find_all("button", {'class':classe_name})

    # classe_name = 'social-details-social-activity.update-v2-social-activity'
    # cmt_soup = linkedin_soup.find_all("div", {'class':classe_name})

    # driver.close()