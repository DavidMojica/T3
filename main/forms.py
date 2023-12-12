from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from .models import EPS, CustomUser, TipoUsuario, InfoMiembros, TipoDocumento, EstadoCivil, RegimenSeguridad, Sexo, Etnia
from django import forms


class FiltroUsuarios(forms.Form):
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    id_usuario = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    documento_usuario = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    
    

class FiltroLlamadasForm(forms.Form):
    id_llamada = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    id_profesional = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control '})
    )
    
    documento_paciente = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    fecha_llamada = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    solo_hechas_por_mi = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class FiltroCitasForm(forms.Form):
    id_cita = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    id_profesional = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control '})
    )
    documento_paciente = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_cita = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    solo_hechas_por_mi = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class CustomUserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.all(),
        widget=forms.Select(attrs={'class': 'custom-class form-select', 'id': 'custom-id'}),
        empty_label='Selecciona un tipo de usuario'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'tipo_usuario')






class AutodataForm(forms.ModelForm):
    tipo_documento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo_documento'
        }),
        empty_label="Selecciona tu tipo de documento"
    )
    estado_civil = forms.ModelChoiceField(
        queryset=EstadoCivil.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_estado_civil'
        }),
        empty_label="Selecciona tu estado civil"
    )
    regimen_seguridad = forms.ModelChoiceField(
        queryset=RegimenSeguridad.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_regimen_seguridad'
        }),
        empty_label="Selecciona tu régimen de seguridad"
    )
    sexo = forms.ModelChoiceField(
        queryset=Sexo.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_sexo'
        }),
        empty_label="Selecciona tu sexo"
    )
    etnia = forms.ModelChoiceField(
        queryset=Etnia.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_etnia'
        }),
        empty_label="Selecciona tu Etnia"
    )
    eps = forms.ModelChoiceField(
        queryset=EPS.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_nombre_eps'})
    )

    # Agregar campos restantes con estilos Bootstrap
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nombre'}))
    documento = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_documento'}))
    numero_hijos = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_numero_hijos'}))
    direccion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_direccion'}))
    barrio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_barrio'}))
    celular = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_celular'}))
    sisben = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_sisben'}))
    
    class Meta:
        model = InfoMiembros
        fields = ('nombre', 'tipo_documento', 'documento', 'estado_civil', 'numero_hijos', 'etnia',
                  'direccion', 'barrio', 'celular', 'sisben', 'eps', 'regimen_seguridad', 'sexo',)


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
