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

class DeleteNewPoolTestCase(openAtticTest):

    def test_TC005(self):
        self.login()
        new_pool_name = self.create_pool("replicated", "16", ['rbd'])
        self.WaitNoBackgroundTasks()
        self.delete_pool(new_pool_name)
        self.WaitNoBackgroundTasks()
        # time.sleep(3)

    def test_TC006(self):
        self.login()
        new_pool_name = self.create_pool("erasure", "16", ['rgw'])
        self.WaitNoBackgroundTasks()
        self.delete_pool(new_pool_name)
        self.WaitNoBackgroundTasks()
        # time.sleep(3)

if __name__ == "__main__":
    unittest.main()
