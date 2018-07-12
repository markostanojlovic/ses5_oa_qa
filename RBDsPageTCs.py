import unittest
from selenium import webdriver
from page import LoginPage
from page import PoolsTab
from page import RBDsTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
import re
from selenium.webdriver.common.by import By
import pytest

class TestRBDsPage(unittest.TestCase):
    """
    Test Cases for testing RBDs tab
    """
    def setUp(self):
        # TODO make a class that will select browser
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        chrome_options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver = webdriver.Chrome() # headfull Chrome for debugging 
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
        self.rbds_tab = RBDsTab(self.driver)
        new_img_name = self.rbds_tab.new_rbd_image(new_pool_name)
        assert self.rbds_tab.driver.find_element(By.LINK_TEXT, new_img_name) # TODO find a better solution, what happends when there are 100+ images? 

    @pytest.mark.skip(reason="not possible to create rbd image in EC pool")
    def test_oA008_new_RBD_1G_from_ec_pg_32(self):
        """
        Create RBD image 1GB from newly created pool: EC pgNum=32, app=rbd,cephfs,rgw, EC-overwrite selected
        """
        # CREATING NEW POOL 
        self.poolsTab = PoolsTab(self.driver)
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', pg_num=32, app='rbd rgw cephfs')
        assert self.poolsTab.pool_present(new_pool_name)
        # CREATING NEW RBD IMAGE 
        self.rbds_tab = RBDsTab(self.driver)
        new_img_name = self.rbds_tab.new_rbd_image(new_pool_name, 1)
        assert self.rbds_tab.driver.find_element(By.LINK_TEXT, new_img_name) # TODO find a better solution
    
    @pytest.mark.skip(reason="rbd img delete takes too long - bug#1064194")
    def test_delete_img(self):
        """
        """
        pass
    
    def tearDown(self):
        print(self._testMethodDoc)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
