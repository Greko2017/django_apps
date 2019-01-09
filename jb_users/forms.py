from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from jb_users.models import User as CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email')

class ContactForm(forms.Form):
	full_name = forms.CharField(required=False, label=False)
	email = forms.EmailField(label=False)
	message = forms.CharField(widget=forms.Textarea(attrs={'cols': 15, 'rows': 5}),label=False)