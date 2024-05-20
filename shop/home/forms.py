from django import forms
from django.contrib.auth.forms  import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(UserCreationForm):
    '''create registration form using usercreation from and customuser model, and required field is email.'''
    class Meta:
        model = CustomUser
        fields = ("email",)
        


class CustomAuthenticationForm(AuthenticationForm):
    '''this class authenticate user using custom authentication using athentication form...'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].name = "email"   

           