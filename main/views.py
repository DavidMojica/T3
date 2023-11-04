from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import IntegrityError
from .forms import TrabajadorEditForm, AdministradorEditForm, AutodataForm
from .models import CustomUser, InfoMiembros, InfoPacientes, Pais, Departamento, Municipio, TipoDocumento, Sexo, EPS, PoblacionVulnerable, PsiMotivos, ConductasASeguir, PsiLlamadas, PsiLlamadasConductas, PsiLlamadasMotivos

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

@login_required
def sm_llamadas(request):
    paises = Pais.objects.all()
    departamentos = Departamento.objects.all()
    municipios = Municipio.objects.all()
    tipos_documento = TipoDocumento.objects.all()
    sexos = Sexo.objects.all()
    EPSS = EPS.objects.all()
    poblacion_vulnerable = PoblacionVulnerable.objects.all()
    motivos = PsiMotivos.objects.all()
    conductas = ConductasASeguir.objects.all()
    
    if request.method == "POST":
        print(request.POST)
        nombre = request.POST['nombre']
        tipo_documento = request.POST['tipo_documento']
        documento = request.POST['documento']
        sexo = request.POST['sexo']
        edad = request.POST['edad']
        eps = request.POST['eps']
        direccion = request.POST['direccion']
        pais = request.POST['pais']
        departamento = request.POST['departamento']
        municipio = request.POST['municipio']
        telefono = request.POST['telefono']
        pob_vulnerable = request.POST['poblacion_vulnerable']
        observaciones = request.POST['observaciones']
        seguimiento24= request.POST['seguimiento24']
        seguimiento48= request.POST['seguimiento48']
        seguimiento72= request.POST['seguimiento72']
    
        llamada = PsiLlamadas(
            documento = documento,
            nombre_paciente = nombre,
            fecha_llamada = datetime.now().date(),
            hora = datetime.now().hour,
            observaciones = observaciones,
            seguimiento24 = seguimiento24,
            seguimiento48 = seguimiento48,
            seguimiento72 = seguimiento72,
            dia_semana_id = datetime.now().weekday(),
            id_psicologo_id = request.user.id,
            sexo = sexo,
            edad = edad
        )
        llamada.save()
        id_llamada = llamada.id
        
        ##conductas y motivos
        for conducta in ConductasASeguir.objects.all():
            checkbox_name = f'cond_{conducta.id}'
            if checkbox_name in request.POST:
                llamada_conducta = PsiLlamadasConductas(
                    id_llamada=id_llamada,
                    id_conducta = conducta
                )
                llamada_conducta.save()

        for motivo in PsiMotivos.objects.all():
            checkbox_name = f'mot_{motivo.id}'
            if checkbox_name in request.POST:
                llamada_motivo = PsiLlamadasMotivos(
                    id_llamada = id_llamada,
                    id_motivo = motivo
                )
                llamada_motivo.save()

        ##paciente
        paciente_existe = InfoPacientes.objects.filter(documento = documento).first()

        if paciente_existe:
            #Si el paciente existe se actualizan los datos
            paciente_existe.nombre = nombre
            paciente_existe.tipo_documento = tipo_documento
            paciente_existe.sexo = sexo
            paciente_existe.edad = edad
            paciente_existe.nombre_eps = eps
            paciente_existe.direccion = direccion
            paciente_existe.municipio = municipio
            paciente_existe.poblacion_vulnerable = pob_vulnerable
            paciente_existe.celular = telefono
            paciente_existe.save()
        else:
            ##Si no existe, se crea un paciente nuevo
            nuevo_paciente = InfoPacientes(
                nombre=nombre,
                tipo_documento = tipo_documento,
                sexo = sexo,
                edad = edad,
                nombre_epos = eps,
                direccion = direccion,
                municipio = municipio,
                poblacion_vulnerable = pob_vulnerable,
                celular = telefono
            )
            nuevo_paciente.save()
        
    else:
        pass
    
    return render(request, 'sm_llamadas.html',{'year': datetime.now(),
                                             'CustomUser': request.user,
                                             'paises': paises,
                                             'departamentos': departamentos,
                                             'municipios': municipios,
                                             'tipos_documento': tipos_documento,
                                             'sexos': sexos,
                                             'epss': EPSS,
                                             'poblacion_vulnerable': poblacion_vulnerable,
                                             'motivos':motivos,
                                             'conductas':conductas,
                                             'CustomUser': request.user})

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