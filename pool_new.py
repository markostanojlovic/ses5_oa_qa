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

class NewPoolTestCase(openAtticTest):
    ''' How to call a single test: python file_name.py class_name.method_name
        Example: python pool_new.py NewPoolTestCase.test_t01_replicated
    '''
    def test_TC001(self):
        self.login()
        self.create_pool("replicated", "16", ['rbd'])

    def test_TC002(self):
        self.login()
        self.create_pool("erasure", "16", ['rbd', 'cephfs'])

if __name__ == "__main__":
    unittest.main()
