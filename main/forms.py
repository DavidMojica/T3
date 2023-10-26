from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django import forms

class CustomUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'is_jefe', 'is_trabajador')
        
        
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        
