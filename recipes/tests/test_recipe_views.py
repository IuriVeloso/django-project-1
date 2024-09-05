from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    def test_recipe_home_view_funcion_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_templates_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found!', response.content.decode('utf-8'))
    
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(category_data={'name': 'Cafe da Manha'})
        
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        content = response.content.decode('utf-8')
        
        # Testing some random recipe properties
        self.assertEqual(len(response_recipes), 1)
        self.assertEqual(response_recipes.first().title, 'Recipe Title')
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        
        self.assertEqual(len(response_recipes), 0)
        self.assertIn('No recipes found!', response.content.decode('utf-8'))

    
    def test_recipe_category_view_funcion_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(category_data={'name': 'Jantar'})
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        
        self.assertIn('Jantar', content)
    
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:category', args=(recipe.category.id,)))
        
        self.assertEqual(response.status_code, 404)
    
    
    def test_recipe_detail_view_funcion_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load on recipe'
        
        self.make_recipe(title=needed_title)
        
        response = self.client.get(
            reverse('recipes:recipe',
                    kwargs={
                        'id': 1
                    }))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
    
    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(
            reverse('recipes:recipe',
                    kwargs={
                        'id': recipe.id
                    }))
        
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_search_uses_correct_view_function(self):
        resolved_url = resolve(reverse('recipes:search'))
        self.assertIs(resolved_url.func, views.search)
        
    def test_recipe_search_loads_correct_template(self):
        
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')