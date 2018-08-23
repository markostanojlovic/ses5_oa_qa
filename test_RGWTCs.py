from tests import BaseTest
from rgw import RGWTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import RGWTabLocators
import time

class TestRGWPage(BaseTest):
    """
    Test Cases for RGW tab
    """
    def setUp(self):
        super().setUp()

    def test_oA024_add_rgw_user(self):
        """
        Add new RGW user
        """
        self.rgwTab = RGWTab(self.driver, True)
        username = 'new_rgw_user'
        user_full_name = 'user userovic'
        user_email = 'uuserovic@qalab.com'
        self.rgwTab.add_rgw_user(username, user_full_name, user_email)
        assert self.rgwTab.driver.find_element_by_link_text(username)
