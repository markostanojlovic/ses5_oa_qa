from page import BasePage
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import RbdsTabLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

class RBDsTab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click(MainMenuLocators.RBDS)
        self.wait(CommonTabLocators.REFRESH_BUTTON)

    def new_rbd_image(self,  poolName, imgSize=10, objSize=4, **other):
        """
        Creating a new RBD image.
        Image size is in GB, and object size is in MB. 
        Optional arguments are: 
        rbd_img_name = 'name'
        layering, stripingv2, exclusive-lock, deep-flatten, object-map, journaling, fast-diff  = True | False
        object-map, journaling - requires exclusive-lock # NOT IMPLEMENTED YET
        fast-diff - requires object-map # NOT IMPLEMENTED YET
        """
        self.click(MainMenuLocators.RBDS)
        self.wait(CommonTabLocators.TABLE, 50)
        self.click(RbdsTabLocators.ADD_BUTTON)
        if 'rbd_img_name' in other:
            name = other['rbd_img_name']
        else:
            name_hash_suffix = binascii.hexlify(os.urandom(4))
            name = "qa_rbd_img_" + name_hash_suffix.decode("utf-8")
        self.clear(RbdsTabLocators.NEW_RBD_NAME)
        self.send_keys(RbdsTabLocators.NEW_RBD_NAME, name)
        self.click(RbdsTabLocators.get_pool_locator(poolName))
        self.send_keys(RbdsTabLocators.IMG_SIZE_FIELD, str(imgSize) + "GB")
        self.send_keys(RbdsTabLocators.OBJ_SIZE_FIELD, str(objSize) + "MB")
        feature_list = ['layering', 'stripingv2', 'exclusive-lock', 'deep-flatten', 'object-map', 'journaling' ,'fast-diff']
        if any(key in feature_list for key,value in other.items()):
            self.click(RbdsTabLocators.DEFAULT_FEATURES_CB)
            for opt,value in other.items():
                try:
                    if opt in feature_list:
                        self.checkbox(RbdsTabLocators.get_feature_checkbox_locator(opt))
                except:
                    print("ERROR: Checkbox selection error.")
        self.click(RbdsTabLocators.SUBMIT_BUTTON)
        self.wait(CommonTabLocators.TABLE)
        return name

    def delete_rbd_image(self, imgName, poolName):
        self.click(MainMenuLocators.RBDS)
        self.wait(CommonTabLocators.TABLE)
        self.click(RbdsTabLocators.get_rbd_img_checkbox_locator(imgName))
        # TODO click on delete button
        # TODO type the confirmation text
        # TODO click on delete button 
        # TODO verify that image is deleted 

    def create_snapshot(self, rbd_img_name, **kwargs):
        """
        Creating a snapshot for rbd image.
        Used kwargs: 
            - snapshotname='name'
        """
        if 'snapshotname' in kwargs:
            snapshot_name = kwargs['snapshotname']
        else:
            snapshot_name = 'qa_rbd_snap_test'
        # 3. Select one RBD image by clicking on its' checkbox  
        self.click(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        # 5. Click on create button
        self.click(RbdsTabLocators.SNAP_TABLE_CREATE_BUTTON)
        # 6. Enter a name in pop up form and click on Create button 
        self.wait(RbdsTabLocators.SNAP_NAME_INPUT)
        self.send_keys(RbdsTabLocators.SNAP_NAME_INPUT, snapshot_name)
        self.click(RbdsTabLocators.SNAP_CREATE_BUTTON)
        # 7. Verify that snapshot is available (also verify on cluster with command: rbd -p rbd-test snap ls )
        self.wait(RbdsTabLocators.SNAP_TABLE_CREATE_BUTTON, 90)
        time.sleep(5)
        self.click(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        time.sleep(5)
        soup  = BeautifulSoup(self.wait(RbdsTabLocators.SNAP_TABLE, 60).get_attribute('innerHTML'), 'html.parser')
        snap_list = []
        for row in soup.find_all('tr'):
            snap_list.append(row.find_all('td')[1].text.strip())
            print(row.find_all('td')[1].text.strip())
        assert snapshot_name in snap_list

    def delete_snapshot(self, rbd_img_name, **kwargs):
        """
        Deleting a snapshot for rbd image.
        Used kwargs: 
            - snapshotname='name'
        """
        if 'snapshotname' in kwargs:
            snapshot_name = kwargs['snapshotname']
        else:
            snapshot_name = 'snaptest'
        # 3. Select one RBD image by clicking on its' checkbox  
        self.click(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        # 5. Select the snapshot by clicking on check box next to it's name
        self.checkbox_all(snapshot_name, RbdsTabLocators.SNAP_TABLE_ROWS)
        self.click(RbdsTabLocators.SNAP_TABLE_DELETE_BUTTON)
        # 6. Enter confirmation text and click Delete button on confirmation popup window
        conf_text = self.wait(RbdsTabLocators.SNAP_DELETE_CONF_TEXT).text
        self.send_keys(RbdsTabLocators.SNAP_DELETE_CONF_TEX_INPUT, conf_text)
        self.click(RbdsTabLocators.SNAP_DELETE_BUTTON)
        time.sleep(5) # TODO
        self.wait(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON, 45)
        time.sleep(5) # TODO
        # 7. Verify that snapshot is no longer present (also verify on cluster with command: rbd -p rbd-test snap ls )
        self.wait(RbdsTabLocators.SNAP_TABLE_EMPTY) # TODO 

    def protect_snapshot(self, rbd_img_name, **kwargs):
        """
        Setting up protect flag a snapshot for rbd image. (RBD with layering enabled)
        Used kwargs: 
            - snapshotname='name'
        """
        if 'snapshotname' in kwargs:
            snapshot_name = kwargs['snapshotname']
        else:
            snapshot_name = 'snaptest'
        # 3. Select one RBD image by clicking on its' checkbox  
        self.click(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON, 30)
        # 5. Select the snapshot by clicking on check box next to it's name
        # self.click(RbdsTabLocators.get_rbd_snap_checkbox_locator(snapshot_name)) # TODO why xpath selector not working? 
        self.click(RbdsTabLocators.SNAP_TABLE_FIRST_CB) # TODO temporary workaround !!!
        self.click(RbdsTabLocators.SNAP_TABLE_DDB)
        self.click(RbdsTabLocators.SNAP_PROTECT)
        time.sleep(2)
        self.click(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        self.wait(RbdsTabLocators.SNAP_PROTECT_FLAG_TEXT)

    def clone_snapshot(self, rbd_img_name, **kwargs):
        """
        Coning a snapshot for rbd image. (RBD with layering enabled)
        Used kwargs: 
            - snapshotname='name'
        """
        if 'snapshotname' in kwargs:
            snapshot_name = kwargs['snapshotname']
        else:
            snapshot_name = 'snaptest'
        self.click(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON, 30)
        # 5. Select the snapshot by clicking on check box next to it's name
        # self.click(RbdsTabLocators.get_rbd_snap_checkbox_locator(snapshot_name)) # TODO why xpath selector not working? 
        self.click(RbdsTabLocators.SNAP_TABLE_FIRST_CB) # TODO temporary workaround !!!
        self.click(RbdsTabLocators.SNAP_TABLE_DDB)
        self.click(RbdsTabLocators.SNAP_CLONE)
        self.wait(RbdsTabLocators.SNAP_CLONE_NAME_INPUT)
        self.send_keys(RbdsTabLocators.SNAP_CLONE_NAME_INPUT, 'snaptest_clone')
        self.click(RbdsTabLocators.SNAP_CLONE_CLONE_BUTTON)
        self.wait(CommonTabLocators.REFRESH_BUTTON)
        # TODO verify that element is there in the table 
