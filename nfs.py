from page import BasePage
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import NFSTabLocators
import time

class NFSTab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click(MainMenuLocators.NFS)
        self.wait(CommonTabLocators.ADD_BUTTON) 
    
    def add_nfs_export(self, ceph_path, export_name):
        """
        Add NFS export.
        ceph_path: '/'
        export_name: '/cephfs_qatest/'
        """
        # Click on Add button
        self.click(NFSTabLocators.ADD_BUTTON) 
        self.wait(NFSTabLocators.SUBMIT_BUTTON) 
        # Choose Storage Backend CephFS
        self.click(NFSTabLocators.STORAGE_BACK_DDM)
        self.click(NFSTabLocators.STORAGE_BACK_CEPHFS)
        # Add Ceph path 
        self.send_keys(NFSTabLocators.CEPH_PATH, ceph_path)
        # Add pseudo path
        self.clear(NFSTabLocators.CEPH_PSEUDO)
        self.send_keys(NFSTabLocators.CEPH_PSEUDO, export_name)
        # Select Root squash
        self.click(NFSTabLocators.SQUASH_DDM)
        self.click(NFSTabLocators.SQUASH_ROOT)
        # Submit
        self.click(NFSTabLocators.SUBMIT_BUTTON) 
        # Wait for table to be loaded 
        self.wait(NFSTabLocators.MNG_SERVICE_BUTTON) 

        





