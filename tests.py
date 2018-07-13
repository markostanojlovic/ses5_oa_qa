import unittest
import pytest
from page import LoginPage

@pytest.mark.usefixtures("driver_get")
class BaseTest(unittest.TestCase):
    """
    Base Test Class used for login to the openattic web UI.
    """
    def setUp(self):
        self.loginpage = LoginPage(self.driver)
        self.loginpage.login()

    def tearDown(self):
        print(self._testMethodDoc)
        self.loginpage.logout()
