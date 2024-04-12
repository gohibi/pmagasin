from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class UserForm(UserCreationForm):
    username  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nom utilisateur'}))
    email     = forms.EmailField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Email utilisateur'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mot de passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmez mot de passe'}))

    class Meta:
        model = User
        fields = ['username','email']