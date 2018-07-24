from page import BasePage
from locators import MainMenuLocators
from locators import CommonTabLocators
from locators import ISCSITabLocators
import time

class ISCSITab(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.click(MainMenuLocators.ISCSI)
        self.wait(CommonTabLocators.ADD_BUTTON) 
    
    def add_iscsi_img(self, portal, img, **auth):
        """
        Add iSCSI image on specified portal. 
        portal : FQDN or IP of the portal
        img : "pool_name: image name"
        auth: yes | no 
        """
        # Click on Add button
        self.click(ISCSITabLocators.ADD_BUTTON) 
        self.wait(ISCSITabLocators.SUBMIT_BUTTON) 
        # Add portal
        self.click(ISCSITabLocators.ADD_PORTAL_BUTTON)
        try:
            self.click(ISCSITabLocators.get_portal_locator(portal)) 
        except:
            print('ERROR: Portal not found.')
        # Add image
        self.click(ISCSITabLocators.ADD_IMAGE_BUTTON) 
        try:
            self.click(ISCSITabLocators.get_image_locator(img)) 
        except:
            print('ERROR: Image not found.')
        # Click submit
        time.sleep(2) # TODO
        self.click(ISCSITabLocators.SUBMIT_BUTTON) 
        self.wait(CommonTabLocators.REFRESH_BUTTON)

    def delete_iscsi_img(self, img):
        """
        Delete iSCSI image. 
        """
        self.click(ISCSITabLocators.get_checkbox_locator(img)) 
        self.click(ISCSITabLocators.EDIT_DDB)
        self.click(ISCSITabLocators.DELETE_BUTTON)
        confirmation_text = self.wait(ISCSITabLocators.DELETE_CONFIRMATION_TEXT).text
        self.send_keys(ISCSITabLocators.DELETE_CONFIRMATION_INPUT, confirmation_text) 
        self.click(ISCSITabLocators.DELETE_CONFIRM_BUTTON)
        time.sleep(3) # TODO how to wait till confirmation form is not closed? 



