import unittest
from selenium import webdriver
from page import LoginPage
from page import PoolsTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
import re, time
import pytest

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

    def test_oA005_del_pool_repl_pg_64_rgw(self):
        """
        Create new pool: replicated, pgNum=64, app=rgw
        Delete newly created pool 
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='replicated', repl=3, pg_num=64, app='rgw')
        try:
            assert self.poolsTab.pool_present(new_pool_name, pg_num=64, app='rgw')
        except AssertionError:
            print("Assertion Error: Pool {} not found.".format(new_pool_name))
            exit(1)
        self.poolsTab.delete_pool(new_pool_name)
        # VERIFY THAT POOL IS DELETED
        available_pools_list = self.poolsTab.get_table_column('POOLS', 'Name')
        assert new_pool_name not in available_pools_list

    def test_oA006_del_pool_ec_pg_32_rgw_rbd(self):
        """
        Create new pool: erasure, pgNum=32, app=rgw,rbd
        Delete newly created pool 
        Run with command: python PoolsPageTCs.py TestPoolsPage.test_delete_all_qa_pools -v
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', pg_num=32, app='rgw rbd')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=32, app='rgw rbd')
        time.sleep(5) # wait until pool is created, taks not running TODO find a dynamic way for this  
        self.poolsTab.delete_pool(new_pool_name)
        # VERIFY THAT POOL IS DELETED
        available_pools_list = self.poolsTab.get_table_column('POOLS', 'Name')
        assert new_pool_name not in available_pools_list

    @pytest.mark.skip(reason="this is just a maintanance task - cleanup after suite execution")
    def test_delete_all_qa_pools(self):
        """
        Delete all pools with qa_ prefix by clicking on multiple check boxes. 
        """
        available_pools_list = self.poolsTab.get_table_column('POOLS', 'Name')
        to_be_deleted_list = []
        for pool in available_pools_list:
            if re.match(r'^qa_.*', pool): # make a batter regular expression TODO
                to_be_deleted_list.append(pool)
        print('\n')
        for pool in to_be_deleted_list:
            print(pool) #DEBUG
            self.poolsTab.delete_pool(pool) # TODO works, but not stable, anyway faster is to use check boxes
            time.sleep(3)

    @pytest.mark.skip
    def test_dev(self):
        available_pools_list = self.poolsTab.get_table_column('POOLS', 'Name')
        for i in available_pools_list:
            print(i)

    def tearDown(self):
        print(self._testMethodDoc)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
