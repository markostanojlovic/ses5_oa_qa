from tests import BaseTest
from pools import PoolsTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import PoolsTabLocators
import time
import pytest

class TestPoolsPage(BaseTest):
    """
    Test Cases for Pools tab
    """
    def setUp(self):
        super().setUp()
        self.poolsTab = PoolsTab(self.driver)

    def test_oA001_new_pool_repl_3_pg_16_app_rbd(self):
        """
        Create new pool: replicated, repl=3, pgNum=16, app=rbd
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='replicated', repl=3, pg_num=16, app='rbd', pool_name='qa_test_repl')
        assert self.poolsTab.pool_present(new_pool_name)
        
    def test_oA002_new_pool_ec_pg_16_app_rbd_cephfs(self):
        """
        Create new pool: erasure coded, pgNum=16, app=rbd,cephfs
        """
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', pg_num=16, app='rbd cephfs', pool_name='qa_test_ec')
        assert self.poolsTab.pool_present(new_pool_name)

    def test_oA003_edit_pool_repl(self):
        """
        Edit pool created in test_oA001_new_pool_repl_3_pg_16_app_rbd
        """
        new_pool_name = 'qa_test_repl'
        self.poolsTab.edit_pool(pool_name=new_pool_name, pg_num=32, app='rbd rgw')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=32, app='rbd rgw')

    def test_oA004_edit_pool_ec(self):
        """
        Edit pool created in test_oA002_new_pool_ec_pg_16_app_rbd_cephfs
        """
        new_pool_name = 'qa_test_ec'
        self.poolsTab.edit_pool(pool_name=new_pool_name, pg_num=64, app='rbd rgw cephfs')
        assert self.poolsTab.pool_present(new_pool_name, pg_num=64, app='rbd rgw cephfs')

    def test_oA999_delete_all_qa_pools(self):
        """
        Delete all pools with 'qa_' prefix by clicking on multiple check boxes. 
        This TC covers oA005 and oA006 TCs and doing the cleanup in the same time.
        """
        self.poolsTab.expand_table_100()
        if self.poolsTab.checkbox_all('qa_', PoolsTabLocators.POOLS_TABLE):
            self.poolsTab.delete_selected_pools()
