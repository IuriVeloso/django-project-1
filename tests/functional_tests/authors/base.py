from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_firefox_browser
from selenium.webdriver.common.by import By
import time

class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_firefox_browser()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, qtd=5):
        time.sleep(qtd)
        
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')