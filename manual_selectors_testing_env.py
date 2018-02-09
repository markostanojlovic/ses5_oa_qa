# Environment for manual testing of selectors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import ActionChains
import time, re, os, binascii

driver = webdriver.Chrome()
driver.get('http://192.168.100.155/')
time.sleep(3)
driver.find_element_by_name("username").clear()
driver.find_element_by_name("username").send_keys("openattic")
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("openattic")
driver.find_element_by_xpath("//input[@value='Login']").click()
time.sleep(2)

# **** MOZES I SAM da kllikces dok ne dodjes do stanja koje te zanima !!! ****

elem = driver.find_element_by_xpath("(//span[@class='ng-scope']//span)")
elem.text
