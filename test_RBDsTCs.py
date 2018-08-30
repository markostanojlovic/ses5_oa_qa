from tests import BaseTest
from pools import PoolsTab
from rbds import RBDsTab
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import RbdsTabLocators
from selenium.webdriver.common.by import By
import pytest
import time

class TestRBDsPage(BaseTest):
    """
    Test Cases for testing RBDs tab.
    """
    def setUp(self):
        super().setUp()
        self.rbds_tab = RBDsTab(self.driver)

    def test_oA007_new_RBD_1G_from_repl_pg_16(self):
        """
        Create RBD image 1GB from newly created pool: replicated, pgNum=16, app=rbd
        """
        # CREATING NEW POOL 
        self.poolsTab = PoolsTab(self.driver)
        new_pool_name = 'qa_rbd_test_img_repl'
        self.poolsTab.new_pool(pool_name=new_pool_name, pool_type='replicated', repl=3, pg_num=16, app='rbd')
        assert self.poolsTab.pool_present(new_pool_name)
        # CREATING NEW RBD IMAGE 
        self.rbds_tab.click(MainMenuLocators.RBDS)
        self.rbds_tab.wait(CommonTabLocators.REFRESH_BUTTON)
        new_img_name = 'rbd_test_img'
        self.rbds_tab.new_rbd_image(new_pool_name, imgSize=1, objSize=4, rbd_img_name=new_img_name)
        self.rbds_tab.expand_table_100()
        assert self.rbds_tab.driver.find_element(By.LINK_TEXT, new_img_name)

    @pytest.mark.skip(reason="not possible to create rbd image in EC pool")
    def test_oA008_new_RBD_1G_from_ec_pg_32(self):
        """
        Create RBD image 1GB from newly created pool: EC pgNum=32, app=rbd,cephfs,rgw, EC-overwrite selected
        """
        # CREATING NEW POOL 
        self.poolsTab = PoolsTab(self.driver)
        new_pool_name = self.poolsTab.new_pool(pool_type='erasure', app='rbd')
        assert self.poolsTab.pool_present(new_pool_name)
        # CREATING NEW RBD IMAGE 
        self.rbds_tab = RBDsTab(self.driver)
        new_img_name = 'qa_rbd_test_img_ec'
        self.rbds_tab.new_rbd_image(new_pool_name, imgSize=1, objSize=4, rbd_img_name=new_img_name)
        assert self.rbds_tab.driver.find_element(By.LINK_TEXT, new_img_name) # TODO find a better solution
    
    @pytest.mark.skip(reason="rbd img delete takes too long - bug#1064194")
    def test_delete_img(self):
        pass

    def test_oA038_RBD_snapshot_create(self):
        """
        oA038 RBD snapshot feature - create snapshot
        """
        img_name = 'rbd_test_img'
        self.rbds_tab.create_snapshot(img_name, snapshotname='snaptest')

    def test_oA039_RBD_snapshot_delete(self):
        """
        oA039 RBD snapshot feature - delete snapshot
        """
        img_name = 'rbd_test_img'
        self.rbds_tab.delete_snapshot(img_name, snapshotname='snaptest')

    @pytest.mark.skip
    def test_oA040_RBD_snapshot_protect_and_clone(self):
        """
        RBD snapshot feature - protect and clone (RBD with layering enabled)
        Requirement: 
            - POOL qa_rbd_test_pool EXISTING
            - IMAGE qa_rbd_test_pool NOT EXISTING
        """
        # CREATING NEW RBD IMAGE 
        new_img_name = 'rbd_test_img_le'
        new_pool_name = 'rbd_test_pool'
        self.rbds_tab.new_rbd_image(new_pool_name, imgSize=1, objSize=4, rbd_img_name=new_img_name, layering=True)
        assert self.rbds_tab.driver.find_element(By.LINK_TEXT, new_img_name) # TODO find a better solution, what happends when there are 100+ images? 
        # Create a snapshot
        self.rbds_tab.create_snapshot(new_img_name, snapshotname='snaptest')
        self.rbds_tab.click_button(CommonTabLocators.REFRESH_BUTTON)
        # Protect snapshot 
        self.rbds_tab.protect_snapshot(new_img_name, snapshotname='snaptest')
        # Clone snapshot
        self.rbds_tab.click_button(CommonTabLocators.REFRESH_BUTTON)
        self.rbds_tab.clone_snapshot(new_img_name, snapshotname='snaptest')
