from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from .models import CustomUser, TipoUsuario, InfoMiembros, TipoDocumento, EstadoCivil, RegimenSeguridad, Sexo
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
    first_name = forms.CharField(label="Nombre(s)",
        widget=forms.TextInput(attrs={'class': 'blackout-input', 'placeholder': 'Ingrese su(s) nombre(s)'}))
    last_name = forms.CharField(label="Apellido(s)",
        widget=forms.TextInput(attrs={'class': 'blackout-input', 'placeholder': 'Ingrese su(s) apellido(s)'}))
    email = forms.CharField(label="Correo electronico",
        widget=forms.EmailInput(attrs={'class': 'blackout-input', 'placeholder': 'Ingrese su email'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name', 'email')
        
        
class AutodataForm(forms.ModelForm):
    tipo_documento = forms.ModelChoiceField(
        queryset = TipoDocumento.objects.all(),
        widget = forms.Select(attrs = {
            'class': '',
            'id': ''
        }),
        empty_label = "Selecciona tu tipo de documento"
    )
    estado_civil = forms.ModelChoiceField(
        queryset = EstadoCivil.objects.all(),
        widget = forms.Select(attrs={
            'class': '',
            'id': ''
        }),
        empty_label = "Selecciona tu estado civil"
    )
    regimen_seguridad = forms.ModelChoiceField(
        queryset = RegimenSeguridad.objects.all(),
        widget = forms.Select(attrs = {
            'class': '',
            'id': ''
        }),
        empty_label = "Selecciona tu régimen de seguridad"
    )
    sexo = forms.ModelChoiceField(
        queryset=Sexo.objects.all(),
        widget=forms.Select(attrs={
            'class': '',
            'id': ''
        }),
        empty_label="Selecciona tu sexo"
    )
    class Meta:
        model = InfoMiembros
        fields = ('tipo_documento','documento','estado_civil', 'numero_hijos', 'direccion', 'barrio', 'telefono', 'celular', 'sisben', 'regimen_seguridad','sexo',)
            
        

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
        
