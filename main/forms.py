from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from .models import CustomUser, TipoUsuario
from django import forms

class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirmar contraseña'}))
    tipo_usuario = forms.ModelChoiceField(
        queryset = TipoUsuario.objects.all(),
        widget = forms.Select(attrs={'class': 'custom-class', 'id': 'custom-id'}),
        empty_label="Selecciona un tipo de usuario"
    )
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'tipo_usuario')
        
class TrabajadorEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'blackout-input', 'placeholder': 'Ingrese su(s) nombre(s)'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'blackout-input', 'placeholder': 'Ingrese su(s) apellido(s)'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'blackout-input', 'placeholder': 'Ingrese su email'}))

    
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email')
        
class AdministradorEditForm(forms.ModelForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset = TipoUsuario.objects.all(),
        widget = forms.Select(attrs={'class': 'custom-class', 'id': 'custom-id'}),
        empty_label="Selecciona un tipo de usuario"
    )
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'is_active', 'tipo_usuario')
    
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        
