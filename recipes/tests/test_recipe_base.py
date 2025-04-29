from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe

class RecipeMixin:
    def make_category(self, name='Category'):
        category = Category.objects.create(name=name)
        return category
    
    def make_author(self, 
                    first_name='user', 
                    last_name='name', 
                    username='username',
                    password='123456',
                    email='username@email.com',):
        user = User.objects.create_user(
            first_name=first_name, 
            last_name=last_name, 
            username=username,
            password=password,
            email=email,
        )
        return user
    def make_recipe(self, 
                    category_data=None, 
                    author_data=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutos',
                    servings=5,
                    servings_unit='Porções',
                    preparation_steps='Recipe Preparation Steps',
                    preparation_step_is_html=False,
                    is_published=True,):
        
        if category_data is None:
            category_data = {}
            
        if author_data is None:
            author_data = {}
        
        recipe = Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
        )
        return recipe
    
    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = { 
                      'title': f'Recipe Title {i}',
                      'author_data':{'username': f'u{i}'}, 
                      'slug': f'r{i}'
                      }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self):
        return super().setUp()