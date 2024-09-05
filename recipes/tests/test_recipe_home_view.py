from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

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
