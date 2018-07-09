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
from selenium.webdriver import ActionChains

class PreTestCase(openAtticTest):

    def test_t01(self):
        self.login()
        self.create_pool("replicated", "16", ['cephfs','rbd'])
        time.sleep(3)

    def test_t02(self):
        self.login()
        self.create_pool("replicated", "16", ['rbd','rgw'])
        time.sleep(3)

    def test_t03(self):
        self.login()
        self.create_pool("replicated", "16", ['rbd','cephfs'])
        time.sleep(3)

    def test_t04(self):
        self.login()
        self.create_pool("replicated", "16", ['rbd','rgw','cephfs'])
        self.WaitNoBackgroundTasks()


    def test_t05(self):
        self.login()
        self.create_pool("replicated", "16", ['rgw','cephfs'])
        self.WaitNoBackgroundTasks()


    def test_t06(self):
        self.login()
        self.create_pool("replicated", "16", ['cephfs','rbd','rgw'])
        self.WaitNoBackgroundTasks()


if __name__ == "__main__":
    unittest.main(verbosity=2)
