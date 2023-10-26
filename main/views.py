from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm
from .forms import CustomUserLoginForm
from django.urls import reverse_lazy
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
                return redirect('../')  # Reemplaza 'home' con la URL de éxito adecuada
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../login/')  # Redirige a una página de éxito
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('/')