from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import PoolsTabLocators
from locators import RbdsTabLocators
from locators import ISCSITabLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import yaml
import binascii, os, time, re
from bs4 import BeautifulSoup

# Each class is a separate page of the web app

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        f = open('config.yml', 'r')
        self.config = yaml.load(f)
        self.oa_ip = self.config['openAttic_IP']
        self.timeout = self.config['timeout']
        f.close()

    def hover_over(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def fetch_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_element(self, locator, time=20):
        return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))

    def click_button(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator)).click()

    def checkbox(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator)).click()

    def clear_field(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).clear()

    def send_keys(self, locator, keys):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).send_keys(keys)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    def get_table_column(self, tab, col_name):
        """
        tab = OSDS | RBDS | POOLS | NODES | ...
        col_name = Name | ID | Applications | Placement groups | ...
        """
        self.click_button(getattr(MainMenuLocators, tab))
        # VERIFY THE PAGE IS LOADED
        self.fetch_element(CommonTabLocators.REFRESH_BUTTON)
        # SET MAX NUMBER OF DISPLAYED ELEMENTS - 100 
        self.click_button(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB)
        self.click_button(CommonTabLocators.TABLE_LENGTH_100)
        self.fetch_element(CommonTabLocators.REFRESH_BUTTON)
        # GET VALUES FROM THE TABLE COLUMN
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        column = []
        available_columns = set()
        for row in soup.find_all('tr')[1:]: # skipping the first, header row
            for cell in row.find_all('td')[1:]: # skipping the first column, the select check box button
                available_columns.add(cell.get('ng-show'))
                if col_name in cell.get('ng-show'):
                    column.append(cell.text.strip())
        if len(column) == 0:
            # PRINT AVAILABLE COLUMS
            for i in available_columns:
                print(i)
        return column

class LoginPage(BasePage):
    """
    Defined methods = actions on the page
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("http://" + self.oa_ip)

    def login(self, usr_name='openattic', usr_pass='openattic'):
        self.send_keys(LoginPageLocators.USERNAME, usr_name)
        self.send_keys(LoginPageLocators.PASSWORD, usr_pass)
        self.click_button(LoginPageLocators.LOGIN_BUTTON)

    def logout(self):
        self.click_button(CommonTabLocators.LOGOUT_BUTTON)

class PoolsTab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click_button(MainMenuLocators.POOLS)
        self.fetch_element(PoolsTabLocators.TAB_PAGE_TEXT)

    def new_pool(self, **kwargs):
        """
        Input arguments:
        pool_name = 'name'  
        pool_type = 'replicated'    # "replicated" | "erasure" 
        repl = 3                    # number of replicas in case of replicated pool
        pg_num = 16                 # placement group number 
        app = 'rbd cephfs rgw'      # add it as space separated string 
        """
        if 'pool_name' in kwargs:
            self.new_pool_name = kwargs['pool_name']
        else:
            name_hash_suffix = binascii.hexlify(os.urandom(4))
            self.new_pool_name = "qa_" + kwargs['pool_type'] + "_" + name_hash_suffix.decode("utf-8")
        self.click_button(MainMenuLocators.POOLS)
        self.click_button(CommonTabLocators.ADD_BUTTON)       
        self.send_keys(PoolsTabLocators.NEW_POOL_NAME, self.new_pool_name)
        self.click_button(PoolsTabLocators.NEW_POOL_TYPE_SELECTOR)
        if kwargs['pool_type'] == 'replicated':
            # REPLICATED POOL BRANCH
            self.click_button(PoolsTabLocators.NEW_POOL_TYPE_SELECTOR_REPL)
            self.clear_field(PoolsTabLocators.NEW_POOL_REPL_SIZE)
            self.send_keys(PoolsTabLocators.NEW_POOL_REPL_SIZE, str(kwargs['repl']))
        elif kwargs['pool_type'] == 'erasure':
            # ERASURE CODED POOL BRANCH
            self.click_button(PoolsTabLocators.NEW_POOL_TYPE_SELECTOR_EC)
            self.click_button(PoolsTabLocators.NEW_POOL_EC_PROFILE_DDB)
            self.click_button(PoolsTabLocators.NEW_POOL_EC_PROFILE_DEFAULT)
            self.click_button(PoolsTabLocators.NEW_POOL_EC_CRUSH_RULESET_DDB)
            self.click_button(PoolsTabLocators.NEW_POOL_EC_CRUSH_RULESET_EC) # TODO nece uvek da se pojavi, zavisi da li je kreiran dodatni EC profil
            self.click_button(PoolsTabLocators.NEW_POOL_EC_OWERWRITE_CB)
        else:
            print("Error: No valid pool_type specified.")
            exit(1)
        # NUMBER OF PLACEMENT GROUPS
        self.clear_field(PoolsTabLocators.NEW_POOL_PG_NUM)
        self.send_keys(PoolsTabLocators.NEW_POOL_PG_NUM, str(kwargs['pg_num']))
        # ADDING APPs
        def add_rbd_app():
            self.click_button(PoolsTabLocators.NEW_POOL_APP_RBD)
        def add_rgw_app():
            self.click_button(PoolsTabLocators.NEW_POOL_APP_RGW)
        def add_cephfs_app():
            self.click_button(PoolsTabLocators.NEW_POOL_APP_CEPHFS)
        add_app = {
            'rbd': add_rbd_app,
            'rgw': add_rgw_app,
            'cephfs': add_cephfs_app
        }
        app = kwargs['app']
        for i in range(0,len(app.split())):
            add_app[app.split()[i]]()
            self.click_button(PoolsTabLocators.NEW_POOL_ADD_APP_BUTTON)
        # FINISH CREATING NEW POOL BY CLICKING ON SUBMIT BUTTON
        self.click_button(PoolsTabLocators.NEW_POOL_SUBMIT_BUTTON)
        self.wait_for_element(CommonTabLocators.REFRESH_BUTTON, 45)
        return self.new_pool_name

    def pool_present(self, pool_name, **kwargs):
        self.click_button(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB)
        self.click_button(CommonTabLocators.TABLE_LENGTH_100)
        self.fetch_element(CommonTabLocators.REFRESH_BUTTON) # TODO find a better way to wait until table is loaded
        # CHECK IF PG NUMBER IS AS EXPECTED TODO - maybe better to use bs to scrap table data? 
        # CHECK IF APPLICATION LIST IS AS EXPECTED TODO 
        return self.is_element_present(By.LINK_TEXT, pool_name)

    def edit_pool(self, **kwargs):
        """
        pool_name
        pg_num = 16                 # placement group number - can be only increased 
        app = 'rbd cephfs rgw'      # add it as space separated string 
        """
        self.click_button(MainMenuLocators.POOLS)
        self.click_button((By.LINK_TEXT, kwargs['pool_name']))
        self.clear_field(PoolsTabLocators.NEW_POOL_PG_NUM)
        self.send_keys(PoolsTabLocators.NEW_POOL_PG_NUM, str(kwargs['pg_num']))
        # DISCOVER REGISTRED APPS
        apps= []
        # appsPresentElems = self.driver.find_elements(PoolsTabLocators.APPS)
        appsPresentElems = self.driver.find_elements_by_xpath("//input[@ng-model='appName']")
        for i in appsPresentElems :
            apps.append(i.get_attribute('value'))
        appList = kwargs['app'].split()
        # REMOVE APPS NOT NEEDED
        for i in apps :
            if i not in appList :
                locator = (By.XPATH, "//input[@value='"+i+"']/parent::div//button")
                self.click_button(locator)
        # ADD APPS NOT PRESENT 
        for i in appList :
            if i not in apps :
                locator = (By.CSS_SELECTOR, "option[value=\"string:"+i+"\"]")
                self.click_button(locator)
                self.click_button(PoolsTabLocators.NEW_POOL_ADD_APP_BUTTON)
        self.click_button(PoolsTabLocators.NEW_POOL_SUBMIT_BUTTON)
        self.fetch_element(PoolsTabLocators.MAIN_VIEW)

    def delete_pool(self, pool_name):
        self.click_button(MainMenuLocators.POOLS)
        self.click_button(PoolsTabLocators.get_pool_checkbox_locator(pool_name))
        self.click_button(PoolsTabLocators.EDIT_DDB)
        self.click_button(PoolsTabLocators.DELETE_BUTTON) # TODO why only SOMETIMES fails here? 
        confirmation_text = self.fetch_element(PoolsTabLocators.DELETE_CONFIRMATION_TEXT).text
        self.send_keys(PoolsTabLocators.DELETE_CONFIRMATION_INPUT, confirmation_text)
        self.click_button(PoolsTabLocators.DELETE_YES_BUTTON)
        self.wait_for_element(CommonTabLocators.REFRESH_BUTTON, 30)
        time.sleep(5) # instead of this, find other way to get notified TODO
        
class RBDsTab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click_button(MainMenuLocators.RBDS)
        self.wait_for_element(CommonTabLocators.TABLE, 50) 
        self.click_button(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB)
        self.click_button(CommonTabLocators.TABLE_LENGTH_100)
        self.wait_for_element(CommonTabLocators.REFRESH_BUTTON, 60)

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
        self.click_button(MainMenuLocators.RBDS)
        self.wait_for_element(CommonTabLocators.TABLE, 50)
        self.click_button(RbdsTabLocators.ADD_BUTTON)
        if 'rbd_img_name' in other:
            name = other['rbd_img_name']
        else:
            name_hash_suffix = binascii.hexlify(os.urandom(4))
            name = "qa_rbd_img_" + name_hash_suffix.decode("utf-8")
        self.clear_field(RbdsTabLocators.NEW_RBD_NAME)
        self.send_keys(RbdsTabLocators.NEW_RBD_NAME, name)
        self.click_button(RbdsTabLocators.get_pool_locator(poolName))
        self.send_keys(RbdsTabLocators.IMG_SIZE_FIELD, str(imgSize) + "GB")
        self.send_keys(RbdsTabLocators.OBJ_SIZE_FIELD, str(objSize) + "MB")
        # Other options : layering, stripingv2, exclusive-lock, deep-flatten
        feature_list = ['layering', 'stripingv2', 'exclusive-lock', 'deep-flatten', 'object-map', 'journaling' ,'fast-diff']
        if any(key in feature_list for key,value in other.items()):
            self.click_button(RbdsTabLocators.DEFAULT_FEATURES_CB)
            for opt,value in other.items():
                # time.sleep(2)
                try:
                    if opt in feature_list:
                        self.checkbox(RbdsTabLocators.get_feature_checkbox_locator(opt))
                except:
                    print("ERROR: Checkbox selection error.")
        self.click_button(RbdsTabLocators.SUBMIT_BUTTON)
        self.wait_for_element(CommonTabLocators.TABLE, 30)
        return name

    def delete_rbd_image(self, imgName, poolName):
        self.click_button(MainMenuLocators.RBDS)
        self.wait_for_element(CommonTabLocators.TABLE, 30)
        self.click_button(RbdsTabLocators.get_rbd_img_checkbox_locator(imgName))
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
        self.click_button(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click_button(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait_for_element(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        # 5. Click on create button
        self.click_button(RbdsTabLocators.SNAP_TABLE_CREATE_BUTTON)
        # 6. Enter a name in pop up form and click on Create button 
        self.wait_for_element(RbdsTabLocators.SNAP_NAME_INPUT)
        self.send_keys(RbdsTabLocators.SNAP_NAME_INPUT, snapshot_name)
        self.click_button(RbdsTabLocators.SNAP_CREATE_BUTTON)
        # 7. Verify that snapshot is available (also verify on cluster with command: rbd -p rbd-test snap ls )
        self.wait_for_element(RbdsTabLocators.SNAP_TABLE_CREATE_BUTTON, 90)
        time.sleep(5)
        self.click_button(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        time.sleep(5)
        soup  = BeautifulSoup(self.wait_for_element(RbdsTabLocators.SNAP_TABLE, 60).get_attribute('innerHTML'), 'html.parser')
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
        self.click_button(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click_button(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait_for_element(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        # 5. Select the snapshot by clicking on check box next to it's name
        # self.click_button(RbdsTabLocators.get_rbd_snap_checkbox_locator(snapshot_name)) # TODO why xpath selector not working? 
        self.click_button(RbdsTabLocators.SNAP_TABLE_FIRST_CB) # TODO temporary workaround !!!
        self.click_button(RbdsTabLocators.SNAP_TABLE_DELETE_BUTTON)
        # 6. Enter confirmation text and click Delete button on confirmation popup window
        conf_text = self.wait_for_element(RbdsTabLocators.SNAP_DELETE_CONF_TEXT).text
        self.send_keys(RbdsTabLocators.SNAP_DELETE_CONF_TEX_INPUT, conf_text)
        self.click_button(RbdsTabLocators.SNAP_DELETE_BUTTON)
        time.sleep(5)
        self.wait_for_element(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON, 60)
        time.sleep(5)
        # 7. Verify that snapshot is no longer present (also verify on cluster with command: rbd -p rbd-test snap ls )
        self.wait_for_element(RbdsTabLocators.SNAP_TABLE_EMPTY)

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
        self.click_button(RbdsTabLocators.get_rbd_img_checkbox_locator(rbd_img_name))
        # 4. Click on the tab snapshots 
        self.click_button(RbdsTabLocators.SNAPSHOTS_TAB)
        self.wait_for_element(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON, 30)
        # 5. Select the snapshot by clicking on check box next to it's name
        # self.click_button(RbdsTabLocators.get_rbd_snap_checkbox_locator(snapshot_name)) # TODO why xpath selector not working? 
        self.click_button(RbdsTabLocators.SNAP_TABLE_FIRST_CB) # TODO temporary workaround !!!
        self.click_button(RbdsTabLocators.SNAP_TABLE_DDB)
        self.click_button(RbdsTabLocators.SNAP_PROTECT)
        time.sleep(2)
        self.click_button(RbdsTabLocators.SNAP_TABLE_REFRESH_BUTTON)
        self.wait_for_element(RbdsTabLocators.SNAP_PROTECT_FLAG_TEXT)

    def clone_snapshot(self, rbd_img_name, **kwargs):
        """
        Coning a snapshot for rbd image. (RBD with layering enabled)
        Used kwargs: 
            - snapshotname='name'
        """
        pass


class ISCSITab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click_button(MainMenuLocators.ISCSI)
        self.wait_for_element(CommonTabLocators.ADD_BUTTON) 
    
    def add_iscsi_img(self, portal, img, **auth):
        """
        Add iSCSI image on specified portal. 
        portal : FQDN or IP of the portal
        img : "pool_name: image name"
        auth: yes | no 
        """
        # Click on Add button
        self.click_button(ISCSITabLocators.ADD_BUTTON) 
        self.wait_for_element(ISCSITabLocators.SUBMIT_BUTTON) 
        # Add portal
        self.click_button(ISCSITabLocators.ADD_PORTAL_BUTTON)
        try:
            self.click_button(ISCSITabLocators.get_portal_locator(portal)) 
        except:
            print('ERROR: Portal not found.')
        # Add image
        self.click_button(ISCSITabLocators.ADD_IMAGE_BUTTON) 
        try:
            self.click_button(ISCSITabLocators.get_image_locator(img)) 
        except:
            print('ERROR: Image not found.')
        # Click submit
        time.sleep(2) # TODO why dynamic doesn't work
        self.click_button(ISCSITabLocators.SUBMIT_BUTTON) 
        self.wait_for_element(CommonTabLocators.REFRESH_BUTTON, 20)
        time.sleep(5) # TODO verify that element is in the table 


    def delete_iscsi_img(self, img):
        """
        Delete iSCSI image. 
        """
        self.click_button(ISCSITabLocators.get_checkbox_locator(img)) 
        self.click_button(ISCSITabLocators.EDIT_DDB)
        self.click_button(ISCSITabLocators.DELETE_BUTTON)
        confirmation_text = self.fetch_element(ISCSITabLocators.DELETE_CONFIRMATION_TEXT).text
        self.send_keys(ISCSITabLocators.DELETE_CONFIRMATION_INPUT, confirmation_text) 
        self.click_button(ISCSITabLocators.DELETE_CONFIRM_BUTTON)
        time.sleep(5) # TODO how to wait till confirmation form is not closed? 



