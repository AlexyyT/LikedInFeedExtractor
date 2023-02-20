from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

driver_path = "C:\\Users\\ATOU\\Downloads\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path)

# your secret credentials:
email = "toulou26@htmail.fr"
password = "AxyTmt26"

# Go to linkedin and login
driver.get('https://www.linkedin.com/login')

# username = driver.find_element(By.ID, "session_key")
# username.send_keys(email)
driver.add_input(By.ID, 'username', email)
driver.add_input(By.ID, 'password', password)
driver.click_button(By.CLASS_NAME, 'sign-in-form__submit_button')


# time.sleep(0.5)
#
# mdp = driver.find_element(By.ID, "session_password")
# mdp.send_keys(password)
#
# time.sleep(0.5)
#
# sign_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
# sign_in_button.click()
# sleep(15)

#driver.find_element(By.ID, "session_password").send_keys(Keys.RETURN)


driver.get("https://www.linkedin.com/company/hippopotamus-fr/posts/?feedView=all")
time.sleep(3)
# find the keywords/location search bars:
#earch_bars = driver.find_elements_by_class_name('scaffold-finite-scroll scaffold-finite-scroll--infinite')
