from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from subprocess import check_output

class NodesNumTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
	self.driver.implicitly_wait(30)
        self.driver.get("http://192.168.100.155/")
	self.verificationErrors = []
	self.accept_next_alert = True

    def test_t01_nodes_num(self):
        self.wait_if_element_present(By.NAME, "username")
        self.driver.find_element_by_name("username").clear()
        self.driver.find_element_by_name("username").send_keys("openattic")
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys("openattic")
        self.driver.find_element_by_xpath("//input[@value='login']").click()
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
	WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Nodes"))).click()
	table = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table.table-striped.table-bordered.table-hover.dataTable.datatable.ng-scope")))
	column_count = len(table.find_elements_by_tag_name("tr"))
	print "Number of nodes: %s" %(column_count-1)
	cmd='ssh root@192.168.100.151 "salt \* test.ping|grep True|wc -l"'
	num_of_nodes=check_output(['bash','-c',cmd]).rstrip()
	print "Asserting number of nodes..."
	self.assertEqual(column_count-1, int(num_of_nodes))

    def test_t02_nodes_num(self):
        self.wait_if_element_present(By.NAME, "username")
        self.driver.find_element_by_name("username").clear()
        self.driver.find_element_by_name("username").send_keys("openattic")
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys("openattic")
        self.driver.find_element_by_xpath("//input[@value='login']").click()
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
	WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Nodes"))).click()
	table = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "table.table.table-striped.table-bordered.table-hover.dataTable.datatable.ng-scope")))
	column_count = len(table.find_elements_by_tag_name("tr"))
	print "Number of nodes: %s" %(column_count-1)
	cmd='ssh root@192.168.100.151 "salt \* test.ping|grep True|wc -l"'
	num_of_nodes=check_output(['bash','-c',cmd]).rstrip()
	print "Asserting number of nodes..."
	self.assertEqual(column_count-1, int(num_of_nodes))

    def wait_if_element_present(self, how, what):
	for i in range(10):
            try:
                if self.is_element_present(how, what): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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

    def tearDown(self):
        self.driver.close()
	self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
