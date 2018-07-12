import unittest
from selenium import webdriver
from page import LoginPage
from locators import LoginPageLocators
from locators import MainMenuLocators
import re

class TestLoginPage(unittest.TestCase):
    """
    Test Cases for login page.
    """
    def setUp(self):
        # TODO make a class that will select browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.loginpage = LoginPage(self.driver)

    def test_TC001_default_login(self):
        """
        Default login test with openattic/openattic credentials. 
        """
        self.loginpage.login()
        self.loginpage.fetch_element(MainMenuLocators.DASHBOARD)

    def tearDown(self):
        print(self._testMethodDoc)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()