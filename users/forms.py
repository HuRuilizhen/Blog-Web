from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignupForm(UserCreationForm):
    sex_type = forms.ChoiceField(choices=Profile.SEX_CHOICES)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class ProfilePersonalHomepageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["personal_homepage"]
