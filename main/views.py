from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import IntegrityError
from .forms import TrabajadorEditForm, AdministradorEditForm, AutodataForm
from .models import CustomUser, InfoMiembros, Pais, Departamento, Municipio, TipoDocumento, Sexo, EPS



@login_required
def sm_llamadas(request):
    paises = Pais.objects.all()
    departamentos = Departamento.objects.all()
    municipios = Municipio.objects.all()
    tipos_documento = TipoDocumento.objects.all()
    sexos = Sexo.objects.all()
    EPSS = EPS.objects.all()
    
    if request.method == "POST":
        pass
    else:
        pass
    
    return render(request, 'sm_llamadas.html',{'year': datetime.now(),
                                             'CustomUser': request.user,
                                             'paises': paises,
                                             'departamentos': departamentos,
                                             'municipios': municipios,
                                             'tipos_documento': tipos_documento,
                                             'sexos': sexos,
                                             'EPSS': EPS})


######### Errors related to register ##########
ERROR_100 = "Las contraseñas no coinciden."
ERROR_101 = "Formulario inválido."
ERROR_102 = "Ya existe un usuario con el mismo nombre de usuario."

####### Login - EDIT #######
ERROR_200 = "Nombre o contraseña inválido."
ERROR_201 = "No se actualizó su contraseña. Contraseña antigua invalida."
ERROR_202 = "Las contraseñas no coinciden"
SUCCESS_100 = "Contraseña actualizada correctamente."
SUCCESS_101 = "Datos guardados correctamente."

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
        return render(request, 'signin.html', {'year': datetime.now()})

def home(request):
    if request.user.is_authenticated:
        # El usuario está autenticado
        return render(request, 'home.html', {'year': datetime.now(),
                                             'CustomUser': request.user})
    else:
        # El usuario no está autenticado
        return render(request, 'home.html', {'year': datetime.now()})

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

                    info_miembros, created = InfoMiembros.objects.get_or_create(id_usuario=user)

                    if created:
                        info_miembros.save()  # Solo guardar si es un objeto nuevo

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
def autodata(request, user_id):
    user = get_object_or_404(InfoMiembros, pk=user_id)
    if request.method == "POST":
        form = AutodataForm(request.POST, instance=user)

        if form.is_valid():
            form.save()  # Guarda los datos si el formulario es válido
        # Si el formulario no es válido, puedes agregar manejo de errores o validaciones personalizadas aquí
            return render(request, 'autodata.html', {
                'CustomUser': request.user,
                'year': datetime.now(),
                'form': form,
                'event' : SUCCESS_101
            })
        else:
            return render(request, 'autodata.html', {
                'CustomUser': request.user,
                'year': datetime.now(),
                'form': form,
                'event' : ERROR_101
            })
    else:
        form = AutodataForm(instance=user)  # En el caso de una solicitud GET, simplemente muestra el formulario

    return render(request, 'autodata.html', {
        'CustomUser': request.user,
        'year': datetime.now(),
        'form': form
    })
    


@login_required
def signout(request):
    logout(request)
    return redirect(reverse('home'))


##########CHECK THE PASSWORDD FUNCION

@login_required
def edit_account(request, user_id, user_type):
    user = get_object_or_404(CustomUser, pk=user_id)
    event = ""
    pass_event = ""

    if request.method == "POST" and user_type in (20, 21, 22):
        if "account_data" in request.POST:
            form = TrabajadorEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                event = "Se actualizaron sus datos correctamente :)."
        elif "change_password" in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('new_password2')
            if user.check_password(old_password):
                if new_password == new_password2:
                    user.set_password(new_password)
                    user.save()
                    pass_event = SUCCESS_100
                else:
                    pass_event = ERROR_202
            else:
                pass_event = ERROR_201
                
        
    if request.method == "post" and user_type in (1, 10, 11, 12):
        form = AdministradorEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    
    else: #GET
        if user_type in (20,21,22):
            form = TrabajadorEditForm(instance=user)
        elif user_type in (1, 10, 11, 12):
            form = AdministradorEditForm

    return render(request, 'edit_account.html', {'form': form,
                                                 'event' : event,
                                                 'pass_event' : pass_event,
                                                 'year': datetime.now(),
                                                 'CustomUser': request.user})


#PSICOLOGIA VISTAS
@login_required
def sm_HPC(request):
    if request.method == "GET":
        return render(request, 'sm_HPC.html')
    

    
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