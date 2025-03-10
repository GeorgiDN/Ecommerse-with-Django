from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, AuthenticationForm
from django.contrib.auth import get_user_model
from ecommerseApp.accounts.models import Profile
User = get_user_model()


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username'}
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ))


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
