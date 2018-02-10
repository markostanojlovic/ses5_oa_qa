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
import os, binascii

class iSCSITestCase(openAtticTest):
    '''
    Various tests for iSCSI app in oA
    '''
    def test_TC009(self):
        self.login()
        pool_name = self.create_pool("replicated", "16", ['rbd'])
        self.WaitNoBackgroundTasks()
        rbd_image_name = self.create_rbd_img(pool_name, "2")
        # time.sleep(3)
        self.iSCSI_create(pool_name, rbd_image_name)

if __name__ == "__main__":
    unittest.main()
