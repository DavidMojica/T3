from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from .forms import CustomUserLoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {
                'error': "Nombre o contraseña inválido.",
                'year': datetime.now(),
                'posted_user': username
            })
        else:
            login(request, user)
            return redirect(reverse('home'))
    else:
        return render(request, 'login.html', {'year': datetime.now(),})

def home(request):
    return render(request, 'home.html',{
        'year': datetime.now
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['password2']:
                user = form.save(commit=False)  # Crear el usuario pero no guardarlo todavía
                user.set_password(request.POST['password'])  # Encriptar la contraseña
                user.save()  # Guardar el usuario en la base de datos
                login(request, user)  # Iniciar sesión automáticamente después del registro
                return redirect(reverse('home'))  # Redirige a una página de éxito
            else:
                return render(request, 'register.html', {
                    'form': CustomUserRegistrationForm,
                    "error": "Password doesn't match"
                })
    else:
        return render(request, 'register.html', {'form': CustomUserRegistrationForm})

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('home'))


#PSICOLOGIA VISTAS
@login_required
def sm_HPC(request):
    if request.method == "GET":
        return render(request, 'sm_HPC.html')
    
@login_required
def sm_llamadas(request):
    if request.method == "GET":
        return render(request, 'sm_atencion_urgencias.html')
    
@login_required
def sm_historial(request):
    if request.method == "GET":
        return render(request, 'sm_historial.html')

#404 VISTAS 
@login_required
def restricted_area_404(request):
    if request.method == "GET":
        return render(request, '404_restricted_area.html')
    
@login_required
def not_deployed_404(request):
    if request.method == "GET":
        return render(request, '404_not_deployed.html')
    
#Admin
@login_required
def admon(request):
    if request.method == "GET":
        return render(request, 'admon.html')