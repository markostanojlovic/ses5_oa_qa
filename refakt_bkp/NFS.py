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

class NFSTestCase(openAtticTest):
    '''
    Creating,editing and deleting NFS exports.
    '''
    def test_TC016(self):
        self.login()
        self.createNFS("root", "first", "cephfs", "true", "true", "rw", "root", "all")

if __name__ == "__main__":
    unittest.main()
