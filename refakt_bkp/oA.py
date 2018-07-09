from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import ActionChains
import unittest, time, re
from subprocess import check_output
import os, binascii

class openAtticTest(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        self.driver.get('http://192.168.100.155/')
        self.verificationErrors = []
        self.accept_next_alert = True

    def wait_if_element_present(self, how, what):
        for i in range(5):
            try:
                if self.is_element_present(how, what): break
            except: pass
            time.sleep(i+1)
        else:
            self.fail("time out")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def login(self, username="openattic", passkey="openattic"):
        self.wait_if_element_present(By.NAME, "username")
        self.driver.find_element_by_name("username").clear()
        self.driver.find_element_by_name("username").send_keys(username)
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys(passkey)
        self.driver.find_element_by_xpath("//input[@value='Login']").click()

    def main_links_present(self):
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Dashboard"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Logout"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "OSDs"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "RBDs"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Pools"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Nodes"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "iSCSI"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "NFS"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Object Gateway"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "CRUSH Map"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "System"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "Notifications"))
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "span.ng-binding"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "openattic"))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, "API-Recorder"))

    def WaitNoBackgroundTasks(self):
        WebDriverWait(self.driver, 25).until(EC.text_to_be_present_in_element((By.XPATH, "(//span[@class='ng-scope']//span)"), 'Background-Tasks'))
        # alternative selector:  a > class="tc_task-queue" > uib-tooltip="No tasks running"

    def create_pool(self, poolType="replicated", pgNum="16", apps=['rbd']):
        '''
        poolType = [ "replicated" | "erasure" ]
        apps = [ "rbd" | "rgw | "cephfs" | "Custom application" ]
        '''
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Pools"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='dataTables_length widget-toolbar'])"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "100"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Add"))).click()
        poolName=WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "poolName")))
        poolName.clear()
        name_hash_suffix=binascii.hexlify(os.urandom(4))
        new_pool_name="qa_"+poolType+"_"+name_hash_suffix
        #new_pool_name="qa_"+poolType+"_"+name_hash_suffix.decode("utf-8") #python3
        poolName.send_keys(new_pool_name)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//select[@id='poolTypes'])"))).click()
        time.sleep(1) # otherwize - replicated_rule doenst get automatically selected
        self.driver.find_element_by_css_selector("option[value=\"string:"+poolType+"\"]").click()
        #self.assertEqual(self.driver.find_element_by_xpath("(//option[@label='replicated_rule'])").get_attribute("selected"), "true")
        # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//option[@label='replicated_rule'])")))
        if poolType == 'erasure':
            self.driver.find_element_by_xpath("(//div[@class='checkbox checkbox-primary']//input)").click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "pgNum"))).clear()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "pgNum"))).send_keys(pgNum)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for i in range(0,len(apps)):
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//option[@label='"+apps[i]+"'])"))).click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//button[@class='btn btn-default tc-add-app'])"))).click()
        # TODO : other settings e.g. compresion type
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-sm.btn-primary.tc_submitButton"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, new_pool_name)))
        self.assertTrue(self.is_element_present(By.LINK_TEXT, new_pool_name))
        return new_pool_name

    def delete_pool(self,poolName):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Pools"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//a[text()='"+poolName+"']/parent::td/parent::tr//input[@type='checkbox'])"))).click()
        # time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//a[@class='btn btn-sm btn-primary dropdown-toggle tc_menudropdown'])"))).click()
        # time.sleep(3)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//li[@class='tc_deleteItem ng-scope'])"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//input[@name='enteredName'])"))).send_keys('yes')
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//button[@class='btn btn-sm btn-primary tc_submitButton'])"))).click()

    def edit_pool(self, poolName, pgNum, appList=['rbd']):
        ''' What is possible to edit (for both replicated and EC pools):
        1. Increase PG number (not possible to decrease)
        2. Add application
        3. Remove application
        '''
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Pools"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, poolName))).click()
        pgNumElem = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "pgNum")))
        pgNumElem.clear()
        pgNumElem.send_keys(pgNum)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # get already present apps
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@ng-model='appName']")))
        apps= []
        appsPresentElems = self.driver.find_elements(By.XPATH, "//input[@ng-model='appName']")
        for i in appsPresentElems :
            apps.append(i.get_attribute('value'))
        # remove apps not needed
        for i in apps :
            if i not in appList :
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@value='"+i+"']/parent::div//button"))).click()
            time.sleep(1)
        # add apps not present
        for i in appList :
            if i not in apps :
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "option[value=\"string:"+i+"\"]"))).click()
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//button[@class='btn btn-default tc-add-app'])"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//button[@class='btn btn-sm btn-primary tc_submitButton'])"))).click()

    def create_rbd_img(self, poolName, imgSize="10", objSize="4", **otherFeatures):
        '''
        Image size is in GB, and object size is in MB.
        '''
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "RBDs"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Ceph RBDs']/ancestor::div//a[@class='btn btn-sm btn-primary tc_add_btn ng-scope']"))).click()
        # WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.LINK_TEXT, "Add"))).click()
        name = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "name")))
        name.clear()
        name_hash_suffix = binascii.hexlify(os.urandom(4))
        newName = "qa_rbd_img_"+name_hash_suffix
        name.send_keys(newName)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//select[@id='pool']/option[contains(@label, '"+poolName+"')]"))).click()
        #self.driver.find_element_by_xpath("//select[@id='pool']/option[contains(@label, '"+poolName+"')]").click()
        sizeElem = self.driver.find_element_by_xpath("//input[@id='size']")
        sizeElem.send_keys(imgSize+"GB")
        objSizeElem = self.driver.find_element_by_xpath("//input[@id='obj_size']")
        objSizeElem.send_keys(objSize+"MB")
        #TODO features selection
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), "+newName+")]")))
        return newName

    # TODO maybe to move here functions porta, image and auth for iSCSI ?

    def iSCSI_create(self, poolName, rbdImgName, auth="noauth"):
        '''
        Creating new iSCSI export
        '''
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "iSCSI"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Ceph iSCSI']/ancestor::div//a[@class='btn btn-sm btn-primary tc_add_btn ng-scope']"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-default btn-label pull-right tc_addPortalButton dropdown-toggle']" ))).click()
        self.driver.find_elements_by_xpath("//a[@class='tc_addPortalItem ng-binding']")[0].click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='images']/parent::span/following-sibling::span/button"))).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), '"+poolName+": "+rbdImgName+"')]"))).click()
        if auth == 'auth':
            WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//*[span='Authentication']"))).click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='user']"))).send_keys('qatest')
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']"))).send_keys('qatest')
        time.sleep(2) # submit is clickable all the time - only displays required fields message if conditions not met
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[span='Submit']"))).click()
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), '"+poolName+":"+rbdImgName+"')]")))
        return poolName+":"+rbdImgName

    def iSCSI_edit(self, target_name, what):
        # what = portal, image, auth
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "iSCSI"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//td[text()='"+target_name+"']"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[span='Edit']"))).click()
        time.sleep(2)
        def portal():
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[span='Add portal']"))).click()
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='tc_addPortalItem ng-binding']"))).click()
        def image():
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[span='Add image']"))).click()
            #taking the first image from the drop down menu
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='tc_addImageItem ng-binding']"))).click()
        def auth():
            WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//*[span='Authentication']"))).click()
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='user']"))).send_keys('qatest')
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']"))).send_keys('qatest')
        opt = {'portal':portal, 'image':image, 'auth':auth}
        opt[what]()
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[span='Submit']"))).click()
        WebDriverWait(self.driver, 100).until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'qa_replicated')]")))

    def createNFS(self, export, host, backend, v3, v4, RW, squash, transProtocol):
        '''
        export          = '/'
        host            = hostname of the NFS-ganesha host
        backend         = 'CephFS' | 'Object Gateway'
        v3              = true | false
        v4              = true | false
        RW              = rw | ro | mdonly | mdonly_ro | none
        quash           = root | all | none
        transProtocol   = udp | tcp | all 
        '''
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@href='#/ceph/nfs']"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Ceph NFS']/ancestor::div//a[@class='btn btn-sm btn-primary tc_add_btn ng-scope']"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//select[@id='host']"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//select[@id='host']/option")))
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//select[@id='fsal']"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//select[@id='fsal']/option[text()='"+backend+"']"))).click()
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='path']"))).send_keys(export)
        time.sleep(5)

    # def editNFS(self, export, host, backend, v3, v4, RW, squash, transProtocol):
    # def deleteNFS(self, export, host, backend):

    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)
