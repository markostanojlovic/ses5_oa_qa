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
    OBJECT_GATEWAY_USERS = (By.XPATH, "//div[@id='bs-example-navbar-collapse-1']//span[text()='Users']")
    OBJECT_GATEWAY_BUCKETS = (By.XPATH, "//div[@id='bs-example-navbar-collapse-1']//span[text()='Buckets']")
    CRUSH_MAP = (By.LINK_TEXT, "CRUSH Map")
    SYSTEM = (By.LINK_TEXT, "System")
    LOGOUT = (By.LINK_TEXT, "Logout")
    NOTIFICATIONS = (By.LINK_TEXT, "Notifications")
    API_RECORDER = (By.LINK_TEXT, "API-Recorder")

class CommonTabLocators:
    ADD_BUTTON = (By.LINK_TEXT, "Add")
    TABLE_LENGTH_CHOOSE_DDB = (By.XPATH, "//div[@class='dataTables_length widget-toolbar']")
    TABLE_LENGTH_2 = (By.LINK_TEXT, "2")
    TABLE_LENGTH_100 = (By.LINK_TEXT, "100")
    REFRESH_BUTTON = (By.XPATH, "//div[@class='widget-toolbar tc_refreshBtn']")
    BACKGROUD_TASKS = (By.XPATH, "//span[@class='ng-scope']//span")
    TABLE = (By.XPATH, "//span[text()='Name']//ancestor::th") # assuming that Name field in the table header is enough
    TABLE_NEXT_PAGE = (By.XPATH, "//span[@class='i fa fa-angle-right']")
    TABLE_FOOTER_INFO = (By.XPATH, "//div[@class='dataTables_info']")
    ALERT = (By.ID, "toasty")
    TABLE_ERROR_HEADING = (By.XPATH, "//h3[@class='panel-title ng-binding']")
    TABLE_ERROR_BODY = (By.XPATH, "//div[@class='panel-body']")
    NOTIFICATIONS_BUTTON = (By.XPATH, "//a[@class='dropdown-toggle'][@title='Recent Notifications']")
    NOTIFICATION_MESSAGES = (By.XPATH, "//a[@class='dropdown-toggle'][@title='Recent Notifications']//ancestor::oa-notifications//ul")
    LOGOUT_BUTTON = (By.XPATH, "//a[@title='Sign Out']")

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
    NEW_POOL_EC_OWERWRITE_CB = (By.XPATH, "//span[text()='EC Overwrite']")
    NEW_POOL_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-sm.btn-primary.tc_submitButton")
    NEW_POOL_EC_PROFILE_DDB = (By.ID, "erasureProfiles")
    NEW_POOL_EC_PROFILE_DEFAULT = (By.XPATH, "//option[@label='default']")
    NEW_POOL_EC_CRUSH_RULESET_DDB = (By.ID, "crushSet")
    NEW_POOL_EC_CRUSH_RULESET_EC = (By.XPATH, "//select[@id='crushSet']//option[@label='erasure-code']")
    APPS = (By.XPATH, "//input[@ng-model='appName']")
    EDIT_DDB = (By.XPATH, "(//a[@class='btn btn-sm btn-primary dropdown-toggle tc_menudropdown'])")
    DELETE_BUTTON = (By.XPATH, "//oadatatable//li[@class='tc_deleteItem ng-scope']//a")
    DELETE_CONFIRMATION_TEXT = (By.XPATH, "//oa-delete-confirmation-modal//kbd[@class='ng-binding ng-scope']")
    DELETE_CONFIRMATION_INPUT = (By.XPATH, "(//input[@name='enteredName'])")
    DELETE_YES_BUTTON = (By.XPATH, "(//button[@class='btn btn-sm btn-primary tc_submitButton'])")
    MAIN_VIEW = (By.XPATH, "//div[@ui-view='main']")
    POOLS_TABLE = (By.XPATH, "//ceph-pools-list//table[@class='table table-striped table-bordered table-hover dataTable datatable ng-scope']//tbody/tr")

    @staticmethod
    def get_pool_checkbox_locator(pool_name):
        return (By.XPATH, "//a[text()='{}']/parent::td/parent::tr//input[@type='checkbox']".format(pool_name))

class RbdsTabLocators:
    ADD_BUTTON = (By.XPATH, "//span[text()='Ceph RBDs']/ancestor::div//a[@class='btn btn-sm btn-primary tc_add_btn ng-scope']")
    NEW_RBD_NAME = (By.ID, "name")
    IMG_SIZE_FIELD = (By.ID, "size")
    OBJ_SIZE_FIELD = (By.ID, "obj_size")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    DEFAULT_FEATURES_CB = (By.XPATH, "//div[@class='panel panel-default']//span[text()='Use default features']")
    SNAPSHOTS_TAB = (By.LINK_TEXT, 'Snapshots')
    SNAP_TABLE_REFRESH_BUTTON = (By.XPATH, "//ceph-rbd-snapshot//div[@class='widget-toolbar tc_refreshBtn']//i[@class='fa fa-lg fa-refresh']")
    SNAP_TABLE_CREATE_BUTTON = (By.XPATH, "//ceph-rbd-snapshot//span[text()='Create']")
    SNAP_TABLE_DELETE_BUTTON = (By.XPATH, "//ceph-rbd-snapshot//span[text()='Delete']")
    SNAP_DELETE_CONF_TEXT = (By.XPATH, "//ceph-rbd-snapshot-delete-modal//kbd")
    SNAP_DELETE_CONF_TEX_INPUT = (By.XPATH, "//ceph-rbd-snapshot-delete-modal//input[@name='enteredName']")
    SNAP_DELETE_BUTTON = (By.XPATH, "//ceph-rbd-snapshot-delete-modal//span[text()='Delete']//ancestor::button")
    SNAP_NAME_INPUT = (By.XPATH, "//div[@class='modal-dialog ']//input[@id='name']")
    SNAP_CREATE_BUTTON = (By.XPATH, "//ceph-rbd-snapshot-create-modal//span[contains(text(), 'Create')]//ancestor::button")
    SNAP_TABLE = (By.XPATH, "//ceph-rbd-snapshot//tbody")
    SNAP_TABLE_EMPTY = (By.XPATH, "//ceph-rbd-snapshot//span[text()='No matching records found']")
    SNAP_TABLE_FIRST_CB = (By.CSS_SELECTOR, "#more > oa-tab-set > div > div.tab-content.ng-scope > ceph-rbd-snapshot > ceph-rbd-snapshot-list > oadatatable > div.dataTables_wrapper > div.table-responsive.dataTables_content > table > tbody > tr > td.ng-scope > input")
    SNAP_TABLE_DDB = (By.XPATH, "//ceph-rbd-snapshot//a[@class='btn btn-sm btn-primary dropdown-toggle tc_menudropdown']")
    SNAP_PROTECT = (By.XPATH, "//ceph-rbd-snapshot//span[text()='Protect']")
    SNAP_CLONE = (By.XPATH, "//ceph-rbd-snapshot//span[text()='Clone']")
    SNAP_PROTECT_FLAG_TEXT = (By.XPATH, "//ceph-rbd-snapshot//tbody//span[text()='PROTECTED']") # TODO this is only for first snapshot
    SNAP_CLONE_NAME_INPUT = (By.XPATH, "//ceph-rbd-form//input[@id='name']")
    SNAP_CLONE_CLONE_BUTTON = (By.XPATH, "//ceph-rbd-form//oa-submit-button//button[@type='submit']")
    SNAP_TABLE_ROWS = (By.XPATH, "//ceph-rbd-snapshot//oadatatable//div[@class='table-responsive dataTables_content']//tbody//tr")

    @staticmethod
    def get_pool_locator(pool_name):
        return (By.XPATH, "//select[@id='pool']/option[contains(@label, '{}')]".format(pool_name))
    @staticmethod
    def get_rbd_img_checkbox_locator(img_name):
        return (By.XPATH, "//a[text()='{}']/ancestor::tr//input[@type='checkbox']".format(img_name))
    @staticmethod
    def get_feature_checkbox_locator(name):
        return (By.ID, name)

class ISCSITabLocators:
    MANAGE_SERVICES_BUTTON = (By.XPATH, "//div[@class='oadatatableactions']//span[text()='Manage service']")
    ADD_BUTTON = (By.XPATH, "//div[@class='oadatatableactions']//span[text()='Add']")
    DELETE_BUTTON = (By.XPATH, "//ul[@class='dropdown-menu oa-dropdown-actions oa-dropdown-menu']//span[text()='Delete']")
    EDIT_DDB = (By.XPATH, "//div[@class='oadatatableactions']//a[@class='btn btn-sm btn-primary dropdown-toggle tc_menudropdown']")
    SUBMIT_BUTTON = (By.XPATH, "//div[@class='panel-footer']//span[text()='Submit']")
    ADD_PORTAL_BUTTON = (By.XPATH, "//span[text()='Add portal']")
    ADD_IMAGE_BUTTON = (By.XPATH, "//span[text()='Add image']")
    DELETE_CONFIRMATION_TEXT = (By.XPATH, "//kbd[contains(text(), 'iqn')]")
    DELETE_CONFIRMATION_INPUT = (By.XPATH, "//form[@role='form']//input[@name='enteredName']")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//form[@role='form']//span[text()='Delete']")

    @staticmethod
    def get_portal_locator(name):
        return (By.XPATH, "//ul[@class='dropdown-menu scrollable-menu pull-right']//a[contains(text(),{})]".format(name))

    @staticmethod
    def get_image_locator(name):
        return (By.XPATH, "//ul[@class='dropdown-menu scrollable-menu pull-right']//a[contains(text(),'{}')]".format(name))

    @staticmethod
    def get_checkbox_locator(name):
        return (By.XPATH, "//td[text()='{}']//ancestor::tr//input[@type='checkbox']".format(name.replace(' ', '')))

class NFSTabLocators:
    ADD_BUTTON = (By.CSS_SELECTOR, 'body > div.container-fluid > div > div > div > ceph-nfs-list > oa-ceph-cluster-loader > span > oa-module-loader > span > span > span > oadatatable > div.dataTables_wrapper > div.dataTables_header.clearfix > div.oadatatableactions > actions > div > a.btn.btn-sm.btn-primary.tc_add_btn.ng-scope')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'body > div.container-fluid > div > div > div > ceph-nfs-form > div > form > div > div.panel-footer > div > oa-submit-button > button')
    STORAGE_BACK_DDM = (By.CSS_SELECTOR, '#fsal')
    STORAGE_BACK_CEPHFS = (By.CSS_SELECTOR, '#fsal > option:nth-child(2)')
    CEPH_PATH = (By.CSS_SELECTOR, '#path')
    CEPH_PSEUDO = (By.CSS_SELECTOR, '#pseudo')
    SQUASH_DDM = (By.CSS_SELECTOR, '#squash')
    SQUASH_ROOT = (By.CSS_SELECTOR, '#squash > option:nth-child(3)')
    MNG_SERVICE_BUTTON = (By.CSS_SELECTOR, 'body > div.container-fluid > div > div > div > ceph-nfs-list > oa-ceph-cluster-loader > span > oa-module-loader > span > span > span > oadatatable > div.dataTables_wrapper > div.dataTables_header.clearfix > div.oadatatableactions > additional-actions > span > button')
    EXPORT_DETAILS = (By.CSS_SELECTOR, '#more > oa-tab-set > div > div.tab-content.ng-scope > ceph-nfs-detail > div > div.panel-body > dl')
    # CHKBOX_TMP = (By.CSS_SELECTOR, 'body > div.container-fluid > div > div > div > ceph-nfs-list > oa-ceph-cluster-loader > span > oa-module-loader > span > span > span > oadatatable > div.dataTables_wrapper > div.table-responsive.dataTables_content > table > tbody > tr:nth-child(3) > td.ng-scope > input')
    DATATABLE = (By.XPATH, '//oadatatable//tbody')
    PSEUDO = (By.CSS_SELECTOR, '#more > oa-tab-set > div > div.tab-content.ng-scope > ceph-nfs-detail > div > div.panel-body > dl > span > dd')
    EDIT_DDB = (By.XPATH, "(//a[@class='btn btn-sm btn-primary dropdown-toggle tc_menudropdown'])")
    DELETE_DDB_BUTTON = (By.XPATH, "//ul[@class='dropdown-menu oa-dropdown-actions oa-dropdown-menu']//span[text()='Delete']")
    DELETE_CONFIRMATION_TEXT = (By.XPATH, "//oa-delete-confirmation-modal//kbd[@class='ng-binding ng-scope']")
    DELETE_CONFIRMATION_INPUT = (By.XPATH, "(//input[@name='enteredName'])")
    DELETE_YES_BUTTON = (By.XPATH, "(//button[@class='btn btn-sm btn-primary tc_submitButton'])")

class RGWTabLocators:
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    FORM_USERNAME = (By.ID, "user_id")
    FORM_FULLNAME = (By.ID, "display_name")
    FORM_EMAIL = (By.ID, "email")

