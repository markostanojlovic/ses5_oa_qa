from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from subprocess import check_output
from oA import openAtticTest

class LoginTestCase(openAtticTest):

    def test_t01_login_and_main_page(self):
	# login with default user name and password
	self.login()
	# check if all links are present on the main page
	self.main_links_present()

if __name__ == "__main__":
    unittest.main()
