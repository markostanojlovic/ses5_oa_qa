from tests import BaseTest
from locators import MainMenuLocators
import pytest

class TestLoginPage(BaseTest):
    """
    Test Cases for login page.
    """
    @pytest.mark.skip(reason="duplicate, login is done on every test case")
    def test_TC001_default_login(self):
        """
        Default login test with openattic/openattic credentials. 
        """
        self.loginpage.wait(MainMenuLocators.DASHBOARD)