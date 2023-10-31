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
        
class CustomUserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','old_password', 'new_password', 'new_password2', 'email')
        exclude = ('id', 'last_login', 'is_superuser','username', 'is_staff', 'is_active', 'date_joined', 'tipo_usuario_id')
    
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        
