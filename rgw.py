from page import BasePage
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import RGWTabLocators
import time

class RGWTab(BasePage):
    def __init__(self, driver, users):
        """
        users argument is False or True
        """
        super().__init__(driver)
        self.click(MainMenuLocators.OBJECT_GATEWAY)
        self.click(MainMenuLocators.OBJECT_GATEWAY_USERS) if users else self.click(MainMenuLocators.OBJECT_GATEWAY_BUCKETS)
        self.wait(CommonTabLocators.ADD_BUTTON) 
    
    def add_rgw_user(self, username, user_full_name, user_email):
        """
        Add Object Gateway user
        """
        # Click on Add button
        self.click(CommonTabLocators.ADD_BUTTON) 
        self.wait(RGWTabLocators.SUBMIT_BUTTON) 
        self.send_keys(RGWTabLocators.FORM_USERNAME, username)
        self.send_keys(RGWTabLocators.FORM_FULLNAME, user_full_name)
        self.send_keys(RGWTabLocators.FORM_EMAIL, user_email)
        self.click(RGWTabLocators.SUBMIT_BUTTON) 
        self.wait(CommonTabLocators.REFRESH_BUTTON)



