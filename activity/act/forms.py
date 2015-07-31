from django import forms
from act.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        help_text = {
            'username': (''),
        }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('avatar',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'display:none'})
        }
