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

class NewRBDTestCase(openAtticTest):
    '''
    Creating new RBD image
    '''
    def test_TC007(self):
        self.login()
        new_pool_name = self.create_pool("replicated", "16", ['rbd'])
        self.WaitNoBackgroundTasks()
        self.create_rbd_img(new_pool_name, "15")

    def test_TC008(self):
        self.login()
        new_pool_name = self.create_pool("erasure", "16", ['rbd','rgw','cephfs'])
        self.WaitNoBackgroundTasks()
        #self.create_rbd_img(new_pool_name, "15")


if __name__ == "__main__":
    unittest.main()
