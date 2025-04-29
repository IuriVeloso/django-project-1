import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_firefox_browser
from recipes.tests.test_recipe_base import RecipeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def sleep(self, seconds=3):
        time.sleep(seconds)
        
    def setUp(self):
        self.browser = make_firefox_browser()
        return super().setUp()
        
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()