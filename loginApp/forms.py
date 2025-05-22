from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomerSignUp
from django import forms


class CustomerSignUpForm(UserCreationForm):
    # username = forms.CharField(required=True, label="Username", widget=forms.TextInput(
    #     attrs={'placeholder': 'username'}))
    email = forms.EmailField(required=False)  # Make email optional
    # password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(
    #     attrs={'placeholder': 'password'}))
    # password2 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(
    #     attrs={'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UpdateCustomerForm(forms.ModelForm):
    information = forms.CharField(widget=forms.Textarea, required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    designation = forms.CharField(required=False)
    phone = forms.IntegerField(required=False)
    address = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomerSignUp
        exclude = ['user']
