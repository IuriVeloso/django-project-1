import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr__new_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr__new_value}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
    
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='Invalid')

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your passworld')
        
    first_name = forms.CharField(
        error_messages={'required':'Write your first name'},
        required=True,
        label = 'First name'
    )
    last_name = forms.CharField(
        error_messages={'required':'Write your last name'},
        label = 'Last name'
    )
    email = forms.EmailField(
        error_messages={'required':'Email is required'},
        label = 'E-mail',
        help_text = 'The e-mail must be valid.'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages = {
            'required': 'Please, repeat your password'
        }
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']
        labels = {
            'username': 'Username',
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        
    # def clean_password(self):
    #     data = self.cleaned_data.get('password')
        
    #     if 'atenção' in data:
    #         raise ValidationError('Não digite "%(value)s" no campo passwrod',
    #                               code='invalid',
    #                               params={'value': 'atenção'})
        
    #     return data
    
    # def clean_first_name(self):
    #     data = self.cleaned_data.get('first_name')
        
    #     if 'John Doe' in data:
    #         raise ValidationError('Não digite "%(value)s" no campo first_name',
    #                               code='invalid',
    #                               params={'value': 'John Doe'})
        
    #     return data
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({'password2': 'Password and password2 must be equal!'})