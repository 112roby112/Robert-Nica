from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from assertpy import soft_assertions, assert_that
import unittest

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Set up the Chrome driver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get("https://practicetestautomation.com/practice-test-login/")
        # Uncomment the line below to maximize the browser window
        # self.driver.maximize_window()
          
    def test_login(self):
        # Wait for the username field to be present
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )  
        # Find the username, password, and login button elements
        username = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "submit")

        # Enter the username and password, then click the login button
        username.send_keys("student")
        password.send_keys("Password123")
        login_button.click()

        # Wait for the "Log out" link to be present
        wait = WebDriverWait(self.driver, 10)
        title = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Log out")))

        # Use soft assertions to verify that the "Log out" link is present
        with soft_assertions():
            assert_that(title).is_true()

    def tearDown(self):
        # Quit the driver and close the browser
        self.driver.quit()

if __name__ == "__main__":
    # Run the test case
    unittest.main()

