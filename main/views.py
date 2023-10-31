from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import IntegrityError
from .forms import CustomUserLoginForm, CustomUserEditForm
from .models import CustomUser


######### Errors related to register ##########
ERROR_100 = "Las contraseñas no coinciden."
ERROR_101 = "Formulario inválido."
ERROR_102 = "Ya existe un usuario con el mismo nombre de usuario."

####### Login #######
ERROR_200 = "Nombre o contraseña inválido."
# Create your views here.

#LOGIN
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'signin.html', {
                'error': ERROR_200,
                'year': datetime.now(),
                'posted_user': username
            })
        else:
            login(request, user)
            return redirect(reverse('home'))
    else:
        return render(request, 'signin.html', {'year': datetime.now(),})

def home(request):
    return render(request, 'home.html',{
        'year': datetime.now()
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['password2']:
                try:
                    user = form.save(commit=False)
                    user.username = request.POST['username'].lower()
                    user.set_password(request.POST['password'])
                    user.save()
                    return redirect(reverse('signin'))
                except IntegrityError:
                    return render(request, 'register.html',{
                        'form': form,
                        "error": ERROR_102
                    })            
            else:
                return render(request, 'register.html', {
                    'form': form,
                    "error": ERROR_101
                })
        else:
            return render(request, 'register.html', {
                'form': form,
                "error": ERROR_100
            })
    else:
        form = CustomUserRegistrationForm()  # Crear una instancia del formulario
        return render(request, 'register.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('home'))

@login_required
def edit_account(request, account_id, user_type_id):
    user = get_object_or_404(CustomUser, pk=account_id)
    
    if request.method == "POST" and user_type_id in (20, 21, 22):
        # Si se envió un formulario, crea una instancia del formulario con los datos del usuario
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            # Procesa y guarda los datos del formulario si es válido
            form.save()
    else:
        # Si es una solicitud GET, crea una instancia del formulario con los datos del usuario
        form = CustomUserEditForm(instance=user)

    return render(request, 'edit_account.html', {'form': form})




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