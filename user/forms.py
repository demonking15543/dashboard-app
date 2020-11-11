from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField


class UserSignupForm(UserCreationForm):
    """user signup form"""


    email = forms.EmailField(required=True)
    contact_no = PhoneNumberField()
    #password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = get_user_model() # active user model in this project
        fields = ['first_name', 'last_name', 'email',  'contact_no', 'password1', 'password2']

    def clean_email(self):
        # Get  user  email address from form field
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            # Unable to find a user, this is fine
            return email
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')      




class UserLoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

        
            



