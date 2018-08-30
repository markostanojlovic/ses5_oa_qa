from page import BasePage
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import PoolsTabLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import binascii, os, time

class PoolsTab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click(MainMenuLocators.POOLS)
        self.wait(CommonTabLocators.REFRESH_BUTTON)

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
        self.click(CommonTabLocators.ADD_BUTTON)       
        self.send_keys(PoolsTabLocators.NEW_POOL_NAME, self.new_pool_name)
        self.click(PoolsTabLocators.NEW_POOL_TYPE_SELECTOR)
        if kwargs['pool_type'] == 'replicated':
            # REPLICATED POOL BRANCH
            self.click(PoolsTabLocators.NEW_POOL_TYPE_SELECTOR_REPL)
            self.clear(PoolsTabLocators.NEW_POOL_REPL_SIZE)
            self.send_keys(PoolsTabLocators.NEW_POOL_REPL_SIZE, str(kwargs['repl']))
        elif kwargs['pool_type'] == 'erasure':
            # ERASURE CODED POOL BRANCH
            self.click(PoolsTabLocators.NEW_POOL_TYPE_SELECTOR_EC)
            elem = self.wait(PoolsTabLocators.NEW_POOL_EC_PROFILE_DDB)
            if elem.is_enabled():
                self.click(PoolsTabLocators.NEW_POOL_EC_PROFILE_DEFAULT)
            # elem = self.wait(PoolsTabLocators.NEW_POOL_EC_CRUSH_RULESET_DDB)
            # if elem.is_enabled():
            #     self.click(PoolsTabLocators.NEW_POOL_EC_CRUSH_RULESET_EC) # TODO nece uvek da se pojavi, zavisi da li je kreiran dodatni EC profil
            self.checkbox(PoolsTabLocators.NEW_POOL_EC_OWERWRITE_CB)
        else:
            print("Error: No valid pool_type specified.")
            exit(1)
        # NUMBER OF PLACEMENT GROUPS
        self.clear(PoolsTabLocators.NEW_POOL_PG_NUM)
        self.send_keys(PoolsTabLocators.NEW_POOL_PG_NUM, str(kwargs['pg_num']))
        # ADDING APPs
        def add_rbd_app():
            self.click(PoolsTabLocators.NEW_POOL_APP_RBD)
        def add_rgw_app():
            self.click(PoolsTabLocators.NEW_POOL_APP_RGW)
        def add_cephfs_app():
            self.click(PoolsTabLocators.NEW_POOL_APP_CEPHFS)
        add_app = {
            'rbd': add_rbd_app,
            'rgw': add_rgw_app,
            'cephfs': add_cephfs_app
        }
        app = kwargs['app']
        for i in range(0,len(app.split())):
            add_app[app.split()[i]]()
            self.click(PoolsTabLocators.NEW_POOL_ADD_APP_BUTTON)
        # FINISH CREATING NEW POOL BY CLICKING ON SUBMIT BUTTON
        self.click(PoolsTabLocators.NEW_POOL_SUBMIT_BUTTON)
        self.wait(CommonTabLocators.REFRESH_BUTTON, 60)
        return self.new_pool_name

    def pool_present(self, pool_name, **other):
        self.expand_table_100()
        try:
            self.wait(PoolsTabLocators.get_pool_checkbox_locator(pool_name))
        except:
            print('ERROR: Element not present')
            return False
        # TODO add checking of pg_num and app list
        return True

    def edit_pool(self, **kwargs):
        """
        pool_name
        pg_num = 16                 # placement group number - can be only increased 
        app = 'rbd cephfs rgw'      # add it as space separated string 
        """
        self.click((By.LINK_TEXT, kwargs['pool_name']))
        self.clear(PoolsTabLocators.NEW_POOL_PG_NUM)
        self.send_keys(PoolsTabLocators.NEW_POOL_PG_NUM, str(kwargs['pg_num']))
        # DISCOVER REGISTRED APPS
        apps= []
        appsPresentElems = self.driver.find_elements_by_xpath("//input[@ng-model='appName']")
        for i in appsPresentElems :
            apps.append(i.get_attribute('value'))
        appList = kwargs['app'].split()
        # REMOVE APPS NOT NEEDED
        for i in apps :
            if i not in appList :
                locator = (By.XPATH, "//input[@value='"+i+"']/parent::div//button")
                self.click(locator)
        # ADD APPS NOT PRESENT 
        for i in appList :
            if i not in apps :
                locator = (By.CSS_SELECTOR, "option[value=\"string:"+i+"\"]")
                self.click(locator)
                self.click(PoolsTabLocators.NEW_POOL_ADD_APP_BUTTON)
        self.click(PoolsTabLocators.NEW_POOL_SUBMIT_BUTTON)
        self.wait(CommonTabLocators.REFRESH_BUTTON)

    def checkbox_pool(self, pool_name):
        self.click(PoolsTabLocators.get_pool_checkbox_locator(pool_name))

    def delete_selected_pools(self):
        self.click(PoolsTabLocators.EDIT_DDB)
        self.click(PoolsTabLocators.DELETE_BUTTON) 
        confirmation_text = self.wait(PoolsTabLocators.DELETE_CONFIRMATION_TEXT).text
        self.send_keys(PoolsTabLocators.DELETE_CONFIRMATION_INPUT, confirmation_text)
        self.click(PoolsTabLocators.DELETE_YES_BUTTON)
        self.wait(CommonTabLocators.REFRESH_BUTTON)



        