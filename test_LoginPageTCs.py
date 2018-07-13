import unittest
from selenium import webdriver
from page import LoginPage
from locators import LoginPageLocators
from locators import MainMenuLocators
import re
import pytest

@pytest.mark.usefixtures("driver_get")
class TestLoginPage(unittest.TestCase):
    """
    Test Cases for login page.
    """
    def setUp(self):
        self.loginpage = LoginPage(self.driver)

    def test_TC001_default_login(self):
        """
        Default login test with openattic/openattic credentials. 
        """
        self.loginpage.login()
        self.loginpage.fetch_element(MainMenuLocators.DASHBOARD)

    def tearDown(self):
        print(self._testMethodDoc)
        self.loginpage.logout()

if __name__ == '__main__':
    unittest.main()