from unittest.mock import patch
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found!', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)
        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        search_input = self.browser.find_element(
            By.XPATH, 
            '//input[@placeholder="Busque uma receita...."]'
            )

        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)
        
        self.sleep(1)

        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'recipe-title-container').text
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(20)

        self.browser.get(self.live_server_url)
        
        pagination2 = self.browser.find_element(By.XPATH, '//a[@aria-label="Go to page 2"]')
        
        pagination2.click()
        
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)