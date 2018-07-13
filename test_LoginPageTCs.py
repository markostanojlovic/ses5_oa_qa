from tests import BaseTest
from page import LoginPage
from locators import LoginPageLocators
from locators import MainMenuLocators
import re

class TestLoginPage(BaseTest):
    """
    Test Cases for login page.
    """
    def test_TC001_default_login(self):
        """
        Default login test with openattic/openattic credentials. 
        """
        self.loginpage.fetch_element(MainMenuLocators.DASHBOARD)