from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from .forms import CustomUserLoginForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Create your views here.

def custom_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))  # Reemplaza 'home' con la URL de éxito adecuada
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

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

def a():
    pass