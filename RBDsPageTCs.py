import unittest
from selenium import webdriver
from page import LoginPage
from page import PoolsTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
import re

class TestRBDsPage(unittest.TestCase):
    """
    Test Cases for testing RBDs tab
    """
    def setUp(self):
        # TODO make a class that will select browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        # self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome() # headfull Chrome for debugging 
        self.loginpage = LoginPage(self.driver)
        self.loginpage.login()

    def test_oA007_new_RBD_15G_from_repl_pg_16(self):
        """
        Create RBD image 15GB from newly created pool: replicated, pgNum=16, app=rbd
        """
        # CREATING NEW POOL 
        self.poolsTab = PoolsTab(self.driver)
        new_pool_name = self.poolsTab.new_pool(pool_type='replicated', repl=3, pg_num=16, app='rbd')
        assert self.poolsTab.pool_present(new_pool_name)
        # CREATING NEW RBD IMAGE        

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
