from tests import BaseTest
from page import ISCSITab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import ISCSITabLocators
import pytest
import time

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
        """
        portal = 'hera.qa.suse.cz'
        img = 'rbd-test: test'
        self.iscsiTab.add_iscsi_img(portal, img)

    def test_oA013_remove_iscsi_img(self):
        """
        Remove iSCSI image.
        """
        portal = 'hera.qa.suse.cz'
        img = 'rbd-test: test'
        self.iscsiTab.delete_iscsi_img(img.replace(' ', ''))
        

