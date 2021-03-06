from tests import BaseTest
from iscsi import ISCSITab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import ISCSITabLocators

class TestISCSIPage(BaseTest):
    """
    Test Cases for iSCSI tab
    """
    def setUp(self):
        super().setUp()
        self.iscsiTab = ISCSITab(self.driver)

    def test_oA009_add_iscsi_img_no_auth(self):
        """
        Add iSCSI image without authentication.
        Requirements:
         - PORTAL hera.qa.suse.cz                       is AVAILABLE
         - IMAGE rbd_test_img in POOL rbd_test_pool     is AVAILABLE
        """
        portal = 'hera.qa.suse.cz'
        img = 'rbd_test_pool: rbd_test_img'
        self.iscsiTab.add_iscsi_img(portal, img)

    def test_oA013_remove_iscsi_img(self):
        """
        Remove iSCSI image.
        """
        portal = 'hera.qa.suse.cz'
        img = 'rbd_test_pool: rbd_test_img'
        self.iscsiTab.delete_iscsi_img(img.replace(' ', ''))
        

