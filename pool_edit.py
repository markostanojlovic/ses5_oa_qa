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
from oA import openAtticTest

class EditNewPoolTestCase(openAtticTest):

    def test_TC003(self):
        self.login()
        new_pool_name=self.create_pool("replicated", "16", ['rbd'])
        self.WaitNoBackgroundTasks()
        #WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@ng-model='appName']")))
        # time.sleep(10)
        self.edit_pool(new_pool_name, "32", ['rbd', 'rgw'])
        self.WaitNoBackgroundTasks()
        # time.sleep(3)

    def test_TC004(self):
        self.login()
        new_pool_name=self.create_pool("erasure", "16", ['rbd'])
        self.WaitNoBackgroundTasks()
        # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@ng-model='appName']")))
        self.edit_pool(new_pool_name, "32", ['cephfs', 'rbd'])
        self.WaitNoBackgroundTasks()
        # time.sleep(3)


if __name__ == "__main__":
    unittest.main()
