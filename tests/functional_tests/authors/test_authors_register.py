import pytest
from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def get_form(self):
        return self.browser.find_element_by_xpath('/html/body/a/main/div[2]/form')
    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*20)
    
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        
        self.fill_form_dummy_data(form)
        email_input = form.find_element(By.NAME, 'email')
        email_input.clear()
        email_input.send_keys('dummy@email.com')
        
        callback(form)
        
        return form
    
    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            
            self.sleep(3)
            
            second_form = self.get_form()

            self.assertIn('Write your first name', second_form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            
            self.sleep(3)
            
            second_form = self.get_form()

            self.assertIn('Write your last name', second_form.text)
            
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            
            self.sleep(3)
            
            second_form = self.get_form()

            self.assertIn('This field must not be empty', second_form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.clear()
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            
            self.sleep(3)
            
            second_form = self.get_form()

            self.assertIn('Enter a valid email address', second_form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_password_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')

            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd234')
            password2.send_keys(Keys.ENTER)
            
            self.sleep(3)
            
            second_form = self.get_form()

            self.assertIn('Password and password2 must be equal', second_form.text)
            
        self.form_field_test_with_callback(callback)
        
    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
            
        self.get_by_placeholder(form, 'Ex.: John').send_keys('First')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Last')
        self.get_by_placeholder(form, 'Your username').send_keys('my_username')
        self.get_by_placeholder(form, 'Your e-mail').send_keys('email@valid.cco')
        self.get_by_placeholder(form, 'Type your password').send_keys('P@ssw0rd')
        self.get_by_placeholder(form, 'Repeat your password').send_keys('P@ssw0rd')
        
        form.submit()
        
        self.sleep(1)
        
        self.assertIn(
            'Your user is created! Please, log in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        