import unittest
from selenium import webdriver
from page import LoginPage
from page import PoolsTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
import re

class TestPoolsPage(unittest.TestCase):
    """
    Test Cases for Pools tab
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
        self.poolsTab = PoolsTab(self.driver)

    def test_oA001_new_pool_repl_3_pg_16_app_rbd(self):
        """
        Create new pool: replicated, repl=3, pgNum=16, app=rbd
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='replicated', repl=3, pg_num=16, app='rbd')
        assert self.poolsTab.pool_present(new_pool_name)
        
    def test_oA002_new_pool_ec_pg_16_app_rbd_cephfs(self):
        """
        Create new pool: erasure coded, pgNum=16, app=rbd,cephfs
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', pg_num=16, app='rbd cephfs')
        assert self.poolsTab.pool_present(new_pool_name)

    def test_oA003_edit_pool_repl_3_pg_16_app_rbd(self):
        """
        Create new pool: replicated, repl=3, pgNum=16, app=rbd
        Edit that pool: pgNum=32, app=rbd, rgw
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='replicated', repl=3, pg_num=16, app='rbd')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=16, app='rbd')
        self.poolsTab.edit_pool(pool_name=new_pool_name, pg_num=32, app='rbd rgw')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=32, app='rbd rgw')

    def test_oA004_edit_pool_ec_pg_16_app_rgw(self):
        """
        Create new pool: erasure, pgNum=32, app=rgw
        Edit that pool: pgNum=64, app=rbd, rgw, cephfs
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', pg_num=32, app='rgw')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=32, app='rgw')
        self.poolsTab.edit_pool(pool_name=new_pool_name, pg_num=64, app='rbd rgw cephfs')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=64, app='rbd rgw cephfs')

    def test_oA005_del_pool_repl_pg_24_rgw(self):
        """
        Create new pool: replicated, pgNum=24, app=rgw
        Delete newly created pool 
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='replicated', repl=3, pg_num=24, app='rgw')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=24, app='rgw')
        self.poolsTab.delete_pool(new_pool_name)
        # TODO how to verify that pool is deleted? create list of all pools - use bs? 

    def test_oA006_del_pool_ec_pg_32_rgw_rbd(self):
        """
        Create new pool: erasure, pgNum=32, app=rgw,rbd
        Delete newly created pool 
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', pg_num=32, app='rgw rbd')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=32, app='rgw rbd')
        self.poolsTab.delete_pool(new_pool_name)
        # TODO how to verify that pool is deleted? create list of all pools - use bs? 

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
