from django import forms
from act.models import UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password']:
            self.fields[fieldname].help_text = None


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'Gender', 'Telephone')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'display:none'}),
            'Gender': forms.Select(attrs={'class': 'ui dropdown'}),
        }
