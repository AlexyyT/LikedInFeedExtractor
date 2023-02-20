import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs

def scroll_down_feed(driver,pause):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def get_height(driver):
        return driver.execute_script("return document.body.scrollHeight")

    SCROLL_PAUSE_TIME = pause

    # Get scroll height
    last_height = get_height(driver)

    while True:
        scroll_down(driver)

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = get_height(driver)
        if new_height == last_height:
            break
        last_height = new_height
    pass


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def get_height(driver):
    return driver.execute_script("return document.body.scrollHeight")


def executor(driver, element):
    driver.execute_script("arguments[0].click();", element)


def get_soup(driver):
    page_source = driver.page_source
    soup = bs(page_source, "html")
    return soup


def linkedin_connexion(driver,email,mdp):
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(mdp)
    driver.find_element(By.CLASS_NAME, 'btn__primary--large.from__button--floating').click()


def get_wait(driver, second):
    return driver.WebDriverWait(driver, second)


# def clic_button(driver, By, Text):
#     button = driver.find_element(By, Text)
#     body = driver.find_element(By.CLASS_NAME, 'render-mode-VANILLA.nav-v2.ember-application.icons-loaded.boot-complete')
#     wait = WebDriverWait(driver, 20)
#
#     try:
#         button.click()
#     except:
#         executor(driver, body)
#         try:
#             showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH,
#                                                                    "//button[contains(normalize-space(@class),'t-black--light social-details-social-counts__count-value t-12 hoverable-link-text')]")))
#             showmore_link.click()
#
#         except ElementClickInterceptedException:
#             print("Trying to click on the button again")
#             driver.execute_script("arguments[0].click()", showmore_link)