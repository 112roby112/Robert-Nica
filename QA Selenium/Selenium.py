from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys as keys
from assertpy import soft_assertions, assert_that
import pytest

driver = webdriver.Chrome()
driver.get("https://www.emag.ro")
#driver.maximize_window()

#Locatori
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "searchboxTrigger"))
)

search_bar.send_keys("laptop")
search_bar.send_keys(keys.ENTER)

file_result = driver.find_element(By.CLASS_NAME, "card-v2")
file_result.click()
title = driver.title
print(title)


with soft_assertions():
    assert_that(title).contains("Laptop")  

price = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//p[@class='product-new-price']"))
)
print(price.text)

# click on log-in button
login = driver.find_element(By.ID, "my_account").click()
email_add = driver.find_element(By.ID, "user_login_email").send_keys('robert.nica94@gmail.com')
continue_login = driver.find_element(By.ID, "user_login_continue").click()

login_pass = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "user_login_password"))
).send_keys('parola123')
continue_login_passw = driver.find_element(By.ID, "user_login_continue").click()

try:
    driver.find_element(By.ID, "logout")
    print("Autentificare reușită!")
except:
    print("Autentificare eșuată!")

driver.quit()
