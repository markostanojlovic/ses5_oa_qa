from tests import BaseTest
from nfs import NFSTab
from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import NFSTabLocators
import time

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
        self.nfsTab.wait(NFSTabLocators.DATATABLE).find_elements_by_tag_name('tr')[-1].click()
        elem_export_info = self.nfsTab.wait(NFSTabLocators.EXPORT_DETAILS)
        assert export_name in elem_export_info.text

    def test_oA018_delete_nfs_export(self):
        """
        AdRemove/Delete NFS export
        """
        export_num = len(self.nfsTab.wait(NFSTabLocators.DATATABLE).find_elements_by_tag_name('tr'))
        export_name = '/pseudo_qatest/'
        self.nfsTab.delete_nfs_export(export_name)
        time.sleep(30) # closing delete confirmation window TODO 
        # komplikovano, mora da se napravi custom function: 
        # wait for attribute class='modal-open' of driver.find_element_by_tag_name('body')
        self.nfsTab.wait(CommonTabLocators.REFRESH_BUTTON)
        # verification
        self.nfsTab.expand_table_100()
        new_export_num = len(self.nfsTab.wait(NFSTabLocators.DATATABLE).find_elements_by_tag_name('tr'))
        assert new_export_num + 1 == export_num


