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
    
    def delete_nfs_export(self, export_name):    
        """
        Delete NFS export by it's export name. 
        """  
        found = False
        table_elem = self.wait(NFSTabLocators.DATATABLE)
        for row in table_elem.find_elements_by_tag_name('tr'):
            chkbox = row.find_elements_by_tag_name("td")[0]
            chkbox.click()
            pseudo = self.wait(NFSTabLocators.PSEUDO)
            if pseudo.text == export_name:
                found = True
                # TODO click on Edit DD menu 
                # TODO Click on Delete button
                # TODO Enter confirmation text 
                # TODO Click on Delete button 
            time.sleep(2)
            chkbox.click()
        if not found:
            exit 1




