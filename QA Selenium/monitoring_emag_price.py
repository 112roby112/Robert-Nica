import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

def get_laptop_price():

    price_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "p.product-new-price")))

    raw_price = price_element.get_attribute("textContent")

    clean_price = raw_price.replace("Lei", "").strip().replace(".", "").replace(",", ".")
    
    return float(clean_price)


def search_laptop_price():
    driver.get("https://www.emag.ro/")  
    search_box = driver.find_element(By.NAME, "query")  
    search_box.send_keys("Laptop Apple MacBook Air 13") 
    search_box.send_keys(Keys.RETURN)  #  Enter

    file_result = driver.find_element(By.CLASS_NAME, "card-v2")
    file_result.click()

    
    return 0


search_laptop_price()
previous_price = get_laptop_price()
print(f"Preț inițial: {previous_price} Lei")

while True:
    time.sleep(10)  
    current_price = get_laptop_price()
    
    if  previous_price < (current_price - current_price) * 0.15: # if the price is lower than 15% of the previous price
        print(f" Send sms : {previous_price} Lei → {current_price} Lei")
        previous_price = current_price  # Actualizează prețul precedent
    else:
        print(f" Same price: {current_price} Lei")
