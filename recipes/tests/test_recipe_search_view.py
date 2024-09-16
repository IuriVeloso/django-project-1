from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        resolved_url = resolve(reverse('recipes:search'))
        self.assertIs(resolved_url.func, views.search)
        
    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?search=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?search=teste'
        response = self.client.get(url)
        self.assertIn('Search for &quot;teste&quot;', 
                      response.content.decode('utf-8'))
        
    def test_recipe_search_can_find_recipe_by_title(self):
        title_1 = 'This is recipe one'
        title_2 = 'This is recipe two'
        
        recipe_1 = self.make_recipe(
            title=title_1,
            slug='title-1',
            author_data={'username': 'one'}
        )
        
        recipe_2 = self.make_recipe(
            title=title_2,
            slug='title-2',
            author_data={'username': 'two'}
        )
        
        search_url = reverse('recipes:search')
        response_1 = self.client.get(f'{search_url}?search={title_1}')
        response_2 = self.client.get(f'{search_url}?search={title_2}')
        response_both = self.client.get(f'{search_url}?search=this')
        
        self.assertIn(recipe_1,
                      response_1.context['recipes'])
        self.assertNotIn(recipe_2,
                      response_1.context['recipes'])
        
        # self.assertIn(recipe_2, 
        #               response_2.context['recipes'])
        # self.assertNotIn(recipe_1, 
        #               response_2.context['recipes'])
        
        # self.assertIn(recipe_2, 
        #               response_both.context['recipes'])
        # self.assertIn(recipe_1, 
        #               response_both.context['recipes'])
