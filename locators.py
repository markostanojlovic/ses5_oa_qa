from selenium.webdriver.common.by import By

# USAGE: For each page create a class and define locators for it
# Legend of acronyms:
#       DDB = Drop Down Button
#       CB = Check Box

class LoginPageLocators:
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")

class MainMenuLocators:
    DASHBOARD = (By.LINK_TEXT, "Dashboard")
    OSDS = (By.LINK_TEXT, "OSDs")
    RBDS = (By.LINK_TEXT, "RBDs")
    POOLS = (By.LINK_TEXT, "Pools")
    NODES = (By.LINK_TEXT, "Nodes")
    ISCSI =  (By.LINK_TEXT, "iSCSI")
    NFS = (By.LINK_TEXT, "NFS")
    OBJECT_GATEWAY = (By.LINK_TEXT, "Object Gateway")
    CRUSH_MAP = (By.LINK_TEXT, "CRUSH Map")
    SYSTEM = (By.LINK_TEXT, "System")
    LOGOUT = (By.LINK_TEXT, "Logout")
    NOTIFICATIONS = (By.LINK_TEXT, "Notifications")
    API_RECORDER = (By.LINK_TEXT, "API-Recorder")

class CommonTabLocators:
    ADD_BUTTON = (By.LINK_TEXT, "Add")
    TABLE_LENGTH_CHOOSE_DDB = (By.XPATH, "(//div[@class='dataTables_length widget-toolbar'])") 
    TABLE_LENGTH_100 = (By.LINK_TEXT, "100")
    REFRESH_BUTTON = (By.XPATH, "//div[@class='widget-toolbar tc_refreshBtn']")

class PoolsTabLocators:
    TAB_PAGE_TEXT = (By.XPATH, "//span[text()='Ceph Pools']")
    NEW_POOL_NAME = (By.ID, "poolName")
    NEW_POOL_TYPE_SELECTOR = (By.XPATH, "(//select[@id='poolTypes'])")
    NEW_POOL_TYPE_SELECTOR_REPL = (By.CSS_SELECTOR, "option[value=\"string:replicated\"]")
    NEW_POOL_TYPE_SELECTOR_EC = (By.CSS_SELECTOR, "option[value=\"string:erasure\"]")
    NEW_POOL_PG_NUM = (By.ID, "pgNum")
    NEW_POOL_REPL_SIZE = (By.ID, "size")
    NEW_POOL_APP_RBD = (By.XPATH, "(//option[@label='rbd'])")
    NEW_POOL_APP_RGW = (By.XPATH, "(//option[@label='rgw'])")
    NEW_POOL_APP_CEPHFS = (By.XPATH, "(//option[@label='cephfs'])")
    NEW_POOL_ADD_APP_BUTTON = (By.XPATH, "(//button[@class='btn btn-default tc-add-app'])")
    NEW_POOL_EC_OWERWRITE_CB = (By.XPATH, "//span[text()='EC Overwrite']") # (By.ID, "ec-overwrites") was not working ?
    NEW_POOL_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-sm.btn-primary.tc_submitButton")
    NEW_POOL_EC_PROFILE_DDB = (By.ID, "erasureProfiles")
    NEW_POOL_EC_PROFILE_DEFAULT = (By.XPATH, "//option[@label='default']")
    NEW_POOL_EC_CRUSH_RULESET_DDB = (By.ID, "crushSet")
    NEW_POOL_EC_CRUSH_RULESET_EC = (By.XPATH, "//select[@id='crushSet']//option[@label='erasure-code']")
    APPS = (By.XPATH, "//input[@ng-model='appName']")
    EDIT_DDB = (By.XPATH, "(//a[@class='btn btn-sm btn-primary dropdown-toggle tc_menudropdown'])")
    DELETE_BUTTON = (By.XPATH, "(//li[@class='tc_deleteItem ng-scope'])")
    DELETE_CONFIRMATION_TEXT = (By.XPATH, "//kbd[@class='ng-binding ng-scope']")
    DELETE_CONFIRMATION_INPUT = (By.XPATH, "(//input[@name='enteredName'])")
    DELETE_YES_BUTTON = (By.XPATH, "(//button[@class='btn btn-sm btn-primary tc_submitButton'])")

