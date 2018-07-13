from tests import BaseTest
from page import LoginPage
from page import PoolsTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import PoolsTabLocators
import re, time
from bs4 import BeautifulSoup

class TestBugs(BaseTest):
    """
    Test Cases for reproducing bugs.
    When the test is passed, means that the bug is still active. 
    """
    def test_bug_1100710(self):
        """
        Reproducing bug#1100710
        Bug description: 404 not found when increasing number of rows displayed in a table
        """
        self.poolsTab = PoolsTab(self.driver)
        self.poolsTab.click_button(MainMenuLocators.POOLS)
        # How many pools are dispalyed and what is the total number? 
        print("\n\nDEBUG INFO: {}".format(self.poolsTab.fetch_element(CommonTabLocators.TABLE_FOOTER_INFO).text))
        # How many table rows are displayed per page? 
        print("DEBUG INFO: Rows displayed per page: {}".format(self.poolsTab.fetch_element(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB).text))
        self.poolsTab.click_button(CommonTabLocators.TABLE_NEXT_PAGE)
        # Click on the increase-table-rows-button
        self.poolsTab.click_button(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB)
        # Click on 100
        self.poolsTab.click_button(CommonTabLocators.TABLE_LENGTH_100)
        # Catch the 404 error
        err_header = self.poolsTab.fetch_element(CommonTabLocators.TABLE_ERROR_HEADING).text
        err_body = self.poolsTab.fetch_element(CommonTabLocators.TABLE_ERROR_BODY).text
        print("DEBUG INFO: {} : {} ".format(err_header,err_body))
        # Wait for alert to pass
        time.sleep(8) # TODO dynamically catch this
        # Checking the notifications section
        self.poolsTab.click_button(CommonTabLocators.NOTIFICATIONS_BUTTON)
        notif_html = self.poolsTab.fetch_element(CommonTabLocators.NOTIFICATION_MESSAGES).get_attribute('innerHTML')
        soup = BeautifulSoup(notif_html, 'html.parser')
        msgs = soup.find_all('li')
        if len(msgs) > 0 :
            for msg in msgs:
                print('\n---------------------------')
                print(msg.getText().strip())
                print('\n---------------------------')
