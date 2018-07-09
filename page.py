from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import PoolsTabLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import yaml
import binascii, os

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
        # TODO change from visibility other options
        # TODO add try except
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))

    def click_button(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).click()

    def clear_field(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).clear()

    def send_keys(self, locator, keys):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).send_keys(keys)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

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

class PoolsTab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # self.driver.get("http://" + self.oa_ip + "/openattic/#/ceph/pools")
        self.click_button(MainMenuLocators.POOLS)
        self.fetch_element(PoolsTabLocators.TAB_PAGE_TEXT)

    def new_pool(self, **kwargs):
        """
        Input arguments:
        pool_type = 'replicated'    # "replicated" | "erasure" 
        repl = 3                    # number of replicas in case of replicated pool
        pg_num = 16                 # placement group number 
        app = 'rbd cephfs rgw'      # add it as space separated string 
        """
        self.click_button(MainMenuLocators.POOLS)
        self.click_button(CommonTabLocators.ADD_BUTTON)
        name_hash_suffix = binascii.hexlify(os.urandom(4))
        self.new_pool_name = "qa_" + kwargs['pool_type'] + "_" + name_hash_suffix.decode("utf-8")
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
        return self.new_pool_name

    def pool_present(self, pool_name):
        self.click_button(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB)
        self.click_button(CommonTabLocators.TABLE_LENGTH_100)
        self.fetch_element(CommonTabLocators.REFRESH_BUTTON) # TODO find a better way to wait until table is loaded
        return self.is_element_present(By.LINK_TEXT, pool_name)







