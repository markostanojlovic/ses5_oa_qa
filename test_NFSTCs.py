from tests import BaseTest
from nfs import NFSTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import NFSTabLocators

class TestNFSPage(BaseTest):
    """
    Test Cases for NFS tab
    """
    def setUp(self):
        super().setUp()
        self.nfsTab = NFSTab(self.driver)

    def test_oA016_add_nfs_export(self):
        """
        Add NFS export
        Requirements:
         - ONE NFS-ganesha node    is AVAILABLE
         - CephFS is deployed      is AVAILABLE
        """
        ceph_path = '/'
        export_name = '/pseudo_qatest/'
        self.nfsTab.add_nfs_export(ceph_path, export_name)
        self.nfsTab.click(NFSTabLocators.CHKBOX_TMP)
        elem_export_info = self.nfsTab.wait(NFSTabLocators.EXPORT_DETAILS)
        assert export_name in elem_export_info.text

    def test_oA018_delete_nfs_export(self):
        """
        AdRemove/Delete NFS export
        """
        export_name = '/pseudo_qatest/'
        self.nfsTab.delete_nfs_export(export_name)


