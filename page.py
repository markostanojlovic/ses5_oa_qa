from locators import LoginPageLocators
from locators import MainMenuLocators
from locators import CommonTabLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import yaml
from bs4 import BeautifulSoup

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        f = open('config.yml', 'r')
        self.config = yaml.load(f)
        self.oa_ip = self.config['openAttic_IP']
        self.timeout = self.config['timeout']
        f.close()

    def hover_over(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def wait(self, locator, time=20):
        try:
            return WebDriverWait(self.driver, time).until(EC.visibility_of_element_located(locator))
        except:
            print('ERROR: TIMEOUT for locator: {}'.format(locator))
            exit(1)

    def click(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
        return WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator)).click()

    def checkbox(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator)).click()

    def clear(self, locator):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).clear()

    def send_keys(self, locator, keys):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).send_keys(keys)

    def expand_table_100(self):
        self.click(CommonTabLocators.TABLE_LENGTH_CHOOSE_DDB)
        self.click(CommonTabLocators.TABLE_LENGTH_100)
        self.wait(CommonTabLocators.REFRESH_BUTTON)

    def checkbox_all(self, name_part, locator):
        """
        Returns False if nothing is selected, otherwize returns True
        and selects all checkboxes.
        """
        rows = self.driver.find_elements_by_xpath(locator[1])
        something_is_selected = False
        for r in rows:
            if name_part in r.text:
                r.find_elements('xpath', './td')[0].click()
                something_is_selected = True
        return something_is_selected

    def get_table_column(self, tab, col_name):
        """
        Returns a list of values in specifix table column. 
        tab = OSDS | RBDS | POOLS | NODES | ...
        col_name = Name | ID | Applications | Placement groups | ...
        """
        self.click(getattr(MainMenuLocators, tab))
        self.wait(CommonTabLocators.REFRESH_BUTTON)
        self.expand_table_100()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        column = []
        available_columns = set()
        for row in soup.find_all('tr')[1:]: # skipping the first, header row
            for cell in row.find_all('td')[1:]: # skipping the first column, the select check box button
                available_columns.add(cell.get('ng-show'))
                if col_name in cell.get('ng-show'):
                    column.append(cell.text.strip())
        if len(column) == 0:
            for i in available_columns:
                print(i)
        return column

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("http://" + self.oa_ip)

    def login(self, usr_name='openattic', usr_pass='openattic'):
        self.send_keys(LoginPageLocators.USERNAME, usr_name)
        self.send_keys(LoginPageLocators.PASSWORD, usr_pass)
        self.click(LoginPageLocators.LOGIN_BUTTON)

    def logout(self):
        self.click(CommonTabLocators.LOGOUT_BUTTON)