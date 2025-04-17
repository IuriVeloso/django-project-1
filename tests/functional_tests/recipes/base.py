import time

from django.contrib.staticfiles.testing import LiveServerTestCase
from utils.browser import make_firefox_browser

class RecipeBaseFunctionalTest(LiveServerTestCase):
    def sleep(self, seconds=3):
        time.sleep(seconds)
        
    def setUp(self):
        self.browser = make_firefox_browser()
        return super().setUp()
        
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()