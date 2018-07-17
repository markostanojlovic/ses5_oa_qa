import unittest
import pytest
from page import LoginPage

@pytest.mark.usefixtures("driver_get", "web_driver")
class BaseTest(unittest.TestCase):
    """
    Base Test Class used for login to the openattic web UI.
    """
    def setUp(self):
        self.loginpage = LoginPage(self.driver)
        self.loginpage.login()

    def tearDown(self):
        print(self._testMethodDoc)
        try:
            self.loginpage.logout()
        except:
            print('ERROR: Not possible to logout due to some error.')