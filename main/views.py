from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import IntegrityError, transaction
from django.db.models import Q, Value, CharField
from django.db.models.functions import Cast
from .forms import TrabajadorEditForm, AdministradorEditForm, AutodataForm, FiltroCitasForm, FiltroLlamadasForm, FiltroUsuarios
from .models import SiNoNunca, TipoDocumento, EstatusPersona, SPAActuales, RHPCConductasASeguir, EstatusPersona, HPCMetodosSuicida, RHPCTiposRespuestas, RHPCTiposDemandas, HPC, HPCSituacionContacto, RHPCSituacionContacto, CustomUser, EstadoCivil, InfoMiembros, InfoPacientes, Pais, Departamento, Municipio, TipoDocumento, Sexo, EPS, PoblacionVulnerable, PsiMotivos, ConductasASeguir, PsiLlamadas, PsiLlamadasConductas, PsiLlamadasMotivos, Escolaridad, Lecto1, Lecto2, Calculo, PacienteCalculo, Razonamiento, Etnia, Ocupacion, Pip, PacientePip, RegimenSeguridad, HPCSituacionContacto, HPCTiposDemandas, HPCTiposRespuestas, SPA
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from unidecode import unidecode
import random, string
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

adminOnly = [1, 10]

#Instancias de modelos
paises = Pais.objects.all()
departamentos = Departamento.objects.all()
municipios = Municipio.objects.all()
tipos_documento = TipoDocumento.objects.all()
sexos = Sexo.objects.all()
EPSS = EPS.objects.all()
poblacion_vulnerable = PoblacionVulnerable.objects.all()
motivos = PsiMotivos.objects.all()
conductas = ConductasASeguir.objects.all()
escolaridades = Escolaridad.objects.all()
estados_civiles = EstadoCivil.objects.all()
lectoescritura1 = Lecto1.objects.all()
lectoescritura2 = Lecto2.objects.all()
calculos = Calculo.objects.all()
razonamiento = Razonamiento.objects.all()
etnias = Etnia.objects.all()
ocupaciones = Ocupacion.objects.all()
pips = Pip.objects.all()
regimenes = RegimenSeguridad.objects.all()
hpcsituaciones = HPCSituacionContacto.objects.all()
hpcdemandas = HPCTiposDemandas.objects.all()
hpcrespuestas = HPCTiposRespuestas.objects.all()
spa = SPA.objects.all()
snn = SiNoNunca.objects.all()
ep = EstatusPersona.objects.all()


# Create your views here.

@login_required
def sm_llamadas(request):
    if request.method == "POST":
        ban = True
        error = ""

        nombre = request.POST['nombre']
        documento = request.POST['documento']
        edad = request.POST['edad']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        observaciones = request.POST['observaciones']
        seguimiento24 = request.POST['seguimiento24']
        seguimiento48 = request.POST['seguimiento48']
        seguimiento72 = request.POST['seguimiento72']

        # Campos numericos
        try:
            edad = int(edad)
            if edad < 0:
                ban = False
                error = "La edad debe ser un número positivo."
        except ValueError:
            ban = False
            error = "Error en el formato de la edad."

        # Campos obligatorios
        try:
            tipo_documento = int(request.POST['tipo_documento'])
            sexo = int(request.POST['sexo'])
            eps = int(request.POST['eps'])
            municipio = int(request.POST.get('municipio', 0))
            pob_vulnerable = int(request.POST['poblacion_vulnerable'])
        except ValueError:
            ban = False
            error = "Error en alguno de sus datos. Los campos numéricos deben contener valores válidos."
        if not nombre or not documento or tipo_documento <= 0 or sexo <= 0 or eps <= 0 or pob_vulnerable <= 0:
            ban = False
            error = "Error en alguno de sus datos. Asegúrese de completar todos los campos obligatorios."

        try:
            sexo_instance = Sexo.objects.get(id=sexo)
        except Sexo.DoesNotExist:
            # Manejar el caso donde no se encontró una instancia de Sexo
            sexo_instance = None
        
        try:
            tipo_documento_instance = TipoDocumento.objects.get(
                id=tipo_documento)
        except TipoDocumento.DoesNotExist:
            tipo_documento_instance = None

        try:
            eps_instance = EPS.objects.get(id=eps)
        except EPS.DoesNotExist:
            eps_instance = None

        try:
            municipio_instance = Municipio.objects.get(id=municipio)
        except Municipio.DoesNotExist:
            municipio_instance = None

        try:
            pob_vulnerable_instance = PoblacionVulnerable.objects.get(
                id=pob_vulnerable)
        except PoblacionVulnerable.DoesNotExist:
            pob_vulnerable_instance = None
            
            
        if ban:
            paciente_existe = InfoPacientes.objects.filter(
                documento=documento).first()

            if paciente_existe:
                # Si el paciente existe se actualizan los datos
                paciente_existe.nombre = nombre.lower() if nombre else paciente_existe.nombre
                paciente_existe.tipo_documento = tipo_documento_instance if tipo_documento_instance is not None else paciente_existe.tipo_documento
                paciente_existe.sexo = sexo_instance if sexo_instance is not None else paciente_existe.sexo
                paciente_existe.edad = edad if edad else paciente_existe.edad
                paciente_existe.eps = eps_instance if eps_instance is not None else paciente_existe.eps
                paciente_existe.direccion = direccion.lower() if direccion else paciente_existe.direccion
                paciente_existe.municipio = municipio_instance if municipio_instance is not None else paciente_existe.municipio
                paciente_existe.poblacion_vulnerable = pob_vulnerable_instance if pob_vulnerable is not None else paciente_existe.poblacion_vulnerable
                paciente_existe.celular = telefono if telefono else paciente_existe.celular
                cantidadLlamadas = paciente_existe.cant_llamadas
                paciente_existe.cant_llamadas = cantidadLlamadas + 1
                paciente_existe.save()
            else:
                # Si no existe, se crea un paciente nuevo
                nuevo_paciente = InfoPacientes(
                    nombre=nombre.lower(),
                    documento=documento,
                    tipo_documento=tipo_documento_instance,
                    sexo=sexo_instance,
                    edad=edad,
                    eps=eps_instance,
                    direccion=direccion.lower(),
                    municipio=municipio_instance,
                    poblacion_vulnerable=pob_vulnerable_instance,
                    celular=telefono
                )
                nuevo_paciente.save()
                
            if "secretKey" in request.POST:
                #actualizar llamada
                numLlamada = request.GET.get('llamada', 0)
                llamadaInstance =get_object_or_404(PsiLlamadas, id=numLlamada)
                
                with transaction.atomic():
                    llamadaInstance.observaciones = observaciones
                    llamadaInstance.seguimiento24 = seguimiento24
                    llamadaInstance.seguimiento48 = seguimiento48
                    llamadaInstance.seguimiento72 = seguimiento72
                    llamadaInstance.save()
                
                with transaction.atomic():
                    PsiLlamadasConductas.objects.filter(id_llamada=numLlamada).delete()
                    for conducta in ConductasASeguir.objects.all():
                        checkbox_name = f'cond_{conducta.id}'
                        if checkbox_name in request.POST:
                            try:
                                conducta_instance = ConductasASeguir.objects.get(
                                    id=conducta.id)
                            except ConductasASeguir.DoesNotExist:
                                conducta_instance = None

                            llamada_conducta = PsiLlamadasConductas(
                                id_llamada=llamadaInstance,
                                id_conducta=conducta_instance
                            )
                            llamada_conducta.save()
                            
                with transaction.atomic():
                    PsiLlamadasMotivos.objects.filter(id_llamada=numLlamada).delete()
                    for motivo in PsiMotivos.objects.all():
                        checkbox_name = f'mot_{motivo.id}'
                        if checkbox_name in request.POST:
                            try:
                                motivo_instace = HPCSituacionContacto.objects.get(id=motivo.id)
                            except PsiMotivos.DoesNotExist:
                                motivo_instace = None

                            llamada_motivo = PsiLlamadasMotivos(
                                id_llamada=llamadaInstance,
                                id_motivo=motivo_instace
                            )
                            llamada_motivo.save()
            else:
                #crear nueva llamada
                llamada = PsiLlamadas(
                        documento=documento,
                        nombre_paciente=nombre,
                        observaciones=observaciones,
                        seguimiento24=seguimiento24,
                        seguimiento48=seguimiento48,
                        seguimiento72=seguimiento72,
                        dia_semana_id=datetime.now().weekday(),
                        id_psicologo_id=request.user.id,
                        sexo=sexo_instance,
                        edad=edad
                    )
                llamada.save()
                id_llamada = llamada.id

                try:
                    psi_llamada_instance = PsiLlamadas.objects.get(id=id_llamada)
                except PsiLlamadas.DoesNotExist:
                    psi_llamada_instance = None

                # conductas y motivos
                for conducta in ConductasASeguir.objects.all():
                    checkbox_name = f'cond_{conducta.id}'
                    if checkbox_name in request.POST:
                        try:
                            conducta_instance = ConductasASeguir.objects.get(
                                id=conducta.id)
                        except ConductasASeguir.DoesNotExist:
                            conducta_instance = None

                        llamada_conducta = PsiLlamadasConductas(
                            id_llamada=psi_llamada_instance,
                            id_conducta=conducta_instance
                        )
                        llamada_conducta.save()

                for motivo in PsiMotivos.objects.all():
                    checkbox_name = f'mot_{motivo.id}'
                    if checkbox_name in request.POST:
                        try:
                            motivo_instace = HPCSituacionContacto.objects.get(id=motivo.id)
                        except PsiMotivos.DoesNotExist:
                            motivo_instace = None

                        llamada_motivo = PsiLlamadasMotivos(
                            id_llamada=psi_llamada_instance,
                            id_motivo=motivo_instace
                        )
                        llamada_motivo.save()
            return redirect(reverse('sm_historial_llamadas'))
            
        else:
            return render(request, 'sm_llamadas.html', {'year': datetime.now(),
                                                        'CustomUser': request.user,
                                                        'paises': paises,
                                                        'departamentos': departamentos,
                                                        'municipios': municipios,
                                                        'tipos_documento': tipos_documento,
                                                        'sexos': sexos,
                                                        'epss': EPSS,
                                                        'poblacion_vulnerable': poblacion_vulnerable,
                                                        'CustomUser': request.user,
                                                        'error': error})

    else:
        try:
            llamada = request.GET.get('llamada', 0)
            llamadaWithPaciente = PsiLlamadas.objects.get(id=llamada)
            documento_paciente = llamadaWithPaciente.documento  
            paciente = InfoPacientes.objects.get(documento=documento_paciente)
            
            motivs = PsiLlamadasMotivos.objects.filter(id_llamada_id=llamada).values_list('id_motivo_id', flat=True)
            conducts = PsiLlamadasConductas.objects.filter(id_llamada_id=llamada).values_list('id_conducta_id', flat=True)
            
            
            return render(request, 'sm_llamadas.html', {
                                                'year': datetime.now(),
                                                'CustomUser': request.user,
                                                'paises': paises,
                                                'departamentos': departamentos,
                                                'municipios': municipios,
                                                'tipos_documento': tipos_documento,
                                                'sexos': sexos,
                                                'epss': EPSS,
                                                'poblacion_vulnerable': poblacion_vulnerable,
                                                'motivos': hpcsituaciones,
                                                'conductas': conductas,
                                                'CustomUser': request.user,
                                                'data': llamadaWithPaciente,
                                                'paciente': paciente,
                                                'btnClass': "btn-warning",
                                                'btnText': "Actualizar llamada",
                                                'secretName': "secretKey",
                                                'motivs': motivs,
                                                'conducts': conducts                                                
                                                })
        except:
            return render(request, 'sm_llamadas.html', {'year': datetime.now(),
                                                        'CustomUser': request.user,
                                                        'paises': paises,
                                                        'departamentos': departamentos,
                                                        'municipios': municipios,
                                                        'tipos_documento': tipos_documento,
                                                        'sexos': sexos,
                                                        'epss': EPSS,
                                                        'poblacion_vulnerable': poblacion_vulnerable,
                                                        'CustomUser': request.user,
                                                        'motivos': hpcsituaciones,
                                                        'conductas': conductas,
                                                        'btnClass': "btn-success",
                                                        'btnText': "Guardar llamada",
                                                        })


def get_departamentos(request):
    pais_id = request.GET.get('pais_id')
    if pais_id:
        try:
            pais = get_object_or_404(Pais, id=pais_id)
            departamentos = Departamento.objects.filter(pertenece_pais_id=pais)
            data = [{'id': departamento.id, 'description': departamento.description}
                    for departamento in departamentos]
            return JsonResponse(data, safe=False)
        except Pais.DoesNotExist:
            return JsonResponse([], safe=False)

    return JsonResponse([], safe=False)


def get_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    if departamento_id:
        try:
            departamento = get_object_or_404(Departamento, id=departamento_id)
            municipios = Municipio.objects.filter(
                pertenece_departamento_id=departamento)
            data = [{'id': municipio.id, 'description': municipio.description}
                    for municipio in municipios]
            return JsonResponse(data, safe=False)
        except Departamento.DoesNotExist:
            return JsonResponse([], safe=False)

    return JsonResponse([], safe=False)
# LOGIN


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

                    info_miembros, created = InfoMiembros.objects.get_or_create(
                        id_usuario=user)

                    if created:
                        info_miembros.save()  # Solo guardar si es un objeto nuevo

                    return redirect(reverse('signin'))
                except IntegrityError:
                    return render(request, 'register.html', {
                        'CustomUser': request.user,
                        'form': form,
                        "error": ERROR_102
                    })
            else:
                return render(request, 'register.html', {
                    'CustomUser': request.user,
                    'form': form,
                    "error": ERROR_101
                })
        else:
            return render(request, 'register.html', {
                'CustomUser': request.user,
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
            form.save()
            

            return render(request, 'autodata.html', {
                'CustomUser': request.user,
                'year': datetime.now(),
                'form': form,
                'event': SUCCESS_101
            })
        else:
            return render(request, 'autodata.html', {
                'CustomUser': request.user,
                'year': datetime.now(),
                'form': form,
                'event': ERROR_101
            })
    else:
        # En el caso de una solicitud GET, simplemente muestra el formulario
        form = AutodataForm(instance=user)

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

    else:  # GET
        if user_type in (20, 21, 22):
            form = TrabajadorEditForm(instance=user)
        elif user_type in (1, 10, 11, 12):
            form = AdministradorEditForm

    return render(request, 'edit_account.html', {'form': form,
                                                 'event': event,
                                                 'pass_event': pass_event,
                                                 'year': datetime.now(),
                                                 'CustomUser': request.user})



@login_required
def sm_HPC(request):
    documento = ""
    fecha_nacimiento = None
    if request.method == "POST":
        if "comprobar_documento" in request.POST:
            ban = True
            msg = ""
            documento = request.POST['documento']

            if documento == "" or not documento:
                ban = False
                msg = "Ingrese el documento."

            if (ban):
                try:
                    paciente = InfoPacientes.objects.get(documento=documento)
                    calculosPaciente = PacienteCalculo.objects.filter(documento_usuario=documento).values_list('id_calculo_id', flat=True)
                except InfoPacientes.DoesNotExist:
                    paciente = None
                    calculosPaciente = []
                return render(request, 'sm_HPC.html', {
                    'CustomUser': request.user,
                    'paciente': paciente,
                    'step': 1,
                    'escolaridades': escolaridades,
                    'sexos': sexos,
                    'estados_civil': estados_civiles,
                    'lectoescrituras': lectoescritura1,
                    'lectoescritura_nivel': lectoescritura2,
                    'calculos': calculos,
                    'razonamiento_analitico': razonamiento,
                    'etnias': etnias,
                    'ocupaciones': ocupaciones,
                    'pips': pips,
                    'rsss': regimenes,
                    'epss': EPSS,
                    'year': datetime.now(),
                    'documento': documento,
                    'tipos_documento': tipos_documento,
                    'calculosPaciente': calculosPaciente
                })
            else:
                return render(request, 'sm_HPC.html', {
                    'CustomUser': request.user,
                    'year': datetime.now(),
                    'errorStep0': msg,
                    'step': 0
                })

        elif "actualizar_usuario" in request.POST:
            try:
                documento = request.POST['e_documento']
                ban = True
                error = ""

                paciente = get_object_or_404(
                    InfoPacientes, documento=documento)

                edad = request.POST['e_edad']
                nombre = request.POST['e_nombre']
                fecha_nacimiento = request.POST['e_fecha_nacimiento']
                escolaridad = request.POST['e_escolaridad']
                numero_hijos = request.POST['e_hijos']
                direccion = request.POST['e_direccion']
                barrio = request.POST['e_barrio']
                correo = request.POST['e_correo']
                celular = request.POST['e_celular']

                try:
                    edad = int(edad)
                    if edad < 0:
                        ban = False
                        error = "La edad debe ser un número positivo."
                except ValueError:
                    ban = False
                    error = "Error en el formato de la edad."

                try:
                    fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
                except ValueError:
                    ban = False
                    error = "La fecha de nacimiento debe estar en formato YYYY-MM-DD."
                

                try:
                    tipo_documento = int(request.POST['e_tipo_documento'])
                    sexo = int(request.POST['e_sexo'])
                    estado_civil = int(request.POST['e_estado_civil'])
                    lectoescritura = int(request.POST['e_lect'])
                    lect_nivel = int(request.POST['e_lect2'])
                    raz_analitico = int(request.POST['e_raz_analitico'])
                    etnia = int(request.POST['e_etnia'])
                    ocupacion = int(request.POST['e_ocupacion'])
                    regimen = int(request.POST['e_rss'])

                except ValueError:
                    ban = False
                    error = "Error en alguno de sus datos. Los campos numéricos deben contener valores válidos."

                if not nombre or not sexo or not estado_civil:
                    ban = False
                    error = "Diligencie los campos obligatorios"

                if ban:
                    # Validación simplificada de sisben
                    sisben = request.POST.get('e_sisben') == 'on'

                    # Instancias simplificadas usando get_object_or_404
                    tipo_documento_instance = get_object_or_404(
                        TipoDocumento, id=tipo_documento)
                    escolaridad_instance = get_object_or_404(
                        Escolaridad, id=escolaridad)
                    sexo_instance = get_object_or_404(Sexo, id=sexo)
                    estado_civil_instance = get_object_or_404(
                        EstadoCivil, id=estado_civil)
                    lecto1_instance = get_object_or_404(
                        Lecto1, id=lectoescritura)
                    lecto2_instance = get_object_or_404(Lecto2, id=lect_nivel)
                    razonamiento_instance = get_object_or_404(
                        Razonamiento, id=raz_analitico)
                    etnia_instance = get_object_or_404(Etnia, id=etnia)
                    ocupacion_instance = get_object_or_404(
                        Ocupacion, id=ocupacion)
                    regimen_seguridad_instance = get_object_or_404(
                        RegimenSeguridad, id=regimen)
                    eps_instance = get_object_or_404(
                        EPS, id=request.POST['eps'])

                    # Iniciar una transacción
                    with transaction.atomic():
                        paciente.nombre = nombre
                        paciente.tipo_documento = tipo_documento_instance
                        paciente.fecha_nacimiento = fecha_nacimiento
                        paciente.edad = int(edad)
                        paciente.escolaridad = escolaridad_instance
                        paciente.numero_hijos = numero_hijos
                        paciente.sexo = sexo_instance
                        paciente.direccion = direccion
                        paciente.barrio = barrio
                        paciente.estado_civil = estado_civil_instance
                        paciente.celular = celular
                        paciente.correo = correo
                        paciente.lectoescritura_indicador = lecto1_instance
                        paciente.lectoescritura_nivel = lecto2_instance
                        paciente.razonamiento_analitico = razonamiento_instance
                        paciente.etnia = etnia_instance
                        paciente.ocupacion = ocupacion_instance
                        paciente.regimen_seguridad = regimen_seguridad_instance
                        paciente.sisben = sisben
                        paciente.eps = eps_instance
                        paciente.save()

                    spaActuales = SPAActuales.objects.filter(
                            id_paciente_id=documento).values_list('id_sustancia_id', flat=True)
                    
                    return render(request, 'sm_HPC.html', {
                        'CustomUser': request.user,
                        'year': datetime.now(),
                        'step': 2,
                        'hpcsituaciones': hpcsituaciones,
                        'hpcdemandas': hpcdemandas,
                        'hpcrespuestas': hpcrespuestas,
                        'spa': spa,
                        'snn': snn,
                        'ep': ep,
                        'cas': conductas,
                        'documento': documento,
                        'btnClass': "btn-success",
                        'btnText': "Guardar asesoría",
                        'secretName': "threeCapitor",
                        'spaActuales': spaActuales,
                        'edad_actual':edad
                    })
                else:
                    return render(request, 'sm_HPC.html', {
                        'CustomUser': request.user,
                        'paciente': paciente,
                        'step': 1,
                        'escolaridades': escolaridades,
                        'sexos': sexos,
                        'estados_civil': estados_civiles,
                        'lectoescrituras': lectoescritura1,
                        'lectoescritura_nivel': lectoescritura2,
                        'calculos': calculos,
                        'razonamiento_analitico': razonamiento,
                        'etnias': etnias,
                        'ocupaciones': ocupaciones,
                        'pips': pips,
                        'rsss': regimenes,
                        'epss': EPSS,
                        'year': datetime.now(),
                        'documento': documento,
                        'tipos_documento': tipos_documento,
                        'error': error
                    })

            except (TipoDocumento.DoesNotExist, Escolaridad.DoesNotExist, Sexo.DoesNotExist, EstadoCivil.DoesNotExist, Lecto1.DoesNotExist, Lecto2.DoesNotExist, Razonamiento.DoesNotExist, Etnia.DoesNotExist, Ocupacion.DoesNotExist, RegimenSeguridad.DoesNotExist, EPS.DoesNotExist):
                # Redirigir a una página de detalles del paciente u otra vista después de la actualización
                return render(request, 'sm_HPC.html', {
                    'CustomUser': request.user,
                    'year': datetime.now(),
                    'step': 2,
                    'hpcsituaciones': hpcsituaciones,
                    'hpcdemandas': hpcdemandas,
                    'hpcrespuestas': hpcrespuestas,
                    'spa': spa,
                    'snn': snn,
                    'btnClass': "btn-success",
                    'btnText': "Guardar asesoría",
                    'secretName': "threeCapitor",
                })
        elif "crear_usuario" in request.POST:
            ban = True
            error = ""
            nombre = f"{request.POST['nombre']} {request.POST['apellido']}"
            documento = request.POST.get('documento_bait', None)
            if not documento:
                documento = request.POST.get('documento', None)
            documento = request.POST['documento']
            direccion = request.POST['direccion']
            fecha_nacimiento = request.POST['fecha_nacimiento']
            hijos = request.POST['hijos']
            barrio = request.POST['barrio']
            correo = request.POST['correo']
            celular = request.POST['celular']

            try:
                tipo_documento = int(request.POST['tipo_documento'])
                sexo = int(request.POST['sexo'])
                edad = int(request.POST['edad'])
                eps = int(request.POST['eps'])
                escolaridad = int(request.POST['escolaridad'])
                estado_civil = int(request.POST['estado_civil'])
                lectoescritura = int(request.POST['lectoescritura'])
                raz_analitico = int(request.POST['raz_analitico'])
                lect_nivel = int(request.POST['lect_nivel'])
                ocupacion = int(request.POST['ocupacion'])
                regimen = int(request.POST['rss'])
                etnia = int(request.POST['etnia'])

            except ValueError:
                ban = False
                error = "Error en alguno de sus datos. Los campos numéricos deben contener valores válidos."

            print(
                f"{documento} | {nombre} | {tipo_documento} | {sexo} | {int(request.POST['ocupacion'])} ")
            if not documento or not nombre or not tipo_documento or not sexo or not int(request.POST['ocupacion']):
                ban = False
                error = "Diligencie los campos obligatorios"

            if ban:
                if 'sisben' in request.POST:
                    sisben = True
                else:
                    sisben = False

                try:
                    tipo_documento_instance = TipoDocumento.objects.get(
                        id=tipo_documento)
                except TipoDocumento.DoesNotExist:
                    tipo_documento_instance = None

                try:
                    escolaridad_instance = Escolaridad.objects.get(
                        id=escolaridad)
                except Escolaridad.DoesNotExist:
                    escolaridad_instance = None

                try:
                    sexo_instance = Sexo.objects.get(id=sexo)
                except Sexo.DoesNotExist:
                    sexo_instance = None

                try:
                    estado_civil_instance = EstadoCivil.objects.get(
                        id=estado_civil)
                except EstadoCivil.DoesNotExist:
                    estado_civil_instance = None

                try:
                    lecto1_instance = Lecto1.objects.get(id=lectoescritura)
                except Lecto1.DoesNotExist:
                    lecto1_instance = None
                try:
                    lecto2_instance = Lecto2.objects.get(id=lect_nivel)
                except Lecto2.DoesNotExist:
                    lecto2_instance = None

                try:
                    razonamiento_instance = Razonamiento.objects.get(
                        id=raz_analitico)
                except Razonamiento.DoesNotExist:
                    razonamiento_instance = None

                try:
                    etnia_instance = Etnia.objects.get(id=etnia)
                except:
                    etnia_instance = None

                try:
                    ocupacion_instance = Ocupacion.objects.get(id=ocupacion)
                except:
                    ocupacion_instance = None

                try:
                    regimen_seguridad_instance = RegimenSeguridad.objects.get(
                        id=regimen)
                except:
                    regimen_seguridad_instance = None

                try:
                    eps_instance = EPS.objects.get(id=eps)
                except EPS.DoesNotExist:
                    eps_instance = None

                nuevo_usuario = InfoPacientes(
                    nombre=nombre,
                    documento=documento,
                    tipo_documento=tipo_documento_instance,
                    fecha_nacimiento=fecha_nacimiento,
                    edad=edad,
                    escolaridad=escolaridad_instance,
                    numero_hijos=hijos,
                    sexo=sexo_instance,
                    direccion=direccion,
                    barrio=barrio,
                    estado_civil=estado_civil_instance,
                    celular=celular,
                    email=correo,
                    lectoescritura_indicador=lecto1_instance,
                    lectoescritura_nivel=lecto2_instance,
                    razonamiento_analitico=razonamiento_instance,
                    etnia=etnia_instance,
                    ocupacion=ocupacion_instance,
                    regimen_seguridad=regimen_seguridad_instance,
                    eps=eps_instance,
                    sisben=sisben
                )
                nuevo_usuario.save()

                for c in Calculo.objects.all():
                    checkbox_name = f'calc_{c.id}'
                    if checkbox_name in request.POST:
                        try:
                            calculo_instance = Calculo.objects.get(id=c.id)
                        except Calculo.DoesNotExist:
                            calculo_instance = None

                        calc = PacienteCalculo(
                            documento_usuario=nuevo_usuario,
                            id_calculo=calculo_instance
                        )
                        calc.save()

                for p in Pip.objects.all():
                    checkbox_name = f'pip_{p.id}'
                    if checkbox_name in request.POST:
                        try:
                            pip_instance = Pip.objects.get(id=p.id)
                        except Pip.DoesNotExist:
                            pip_instance = None

                        pp = PacientePip(
                            documento_usuario=nuevo_usuario,
                            id_pip=pip_instance
                        )
                        pp.save()
                        
                spaActuales = SPAActuales.objects.filter(
                            id_paciente_id=documento).values_list('id_sustancia_id', flat=True)
                
                return render(request, 'sm_HPC.html', {
                    'CustomUser': request.user,
                    'year': datetime.now(),
                    'step': 2,
                    'hpcsituaciones': hpcsituaciones,
                    'hpcdemandas': hpcdemandas,
                    'hpcrespuestas': hpcrespuestas,
                    'spa': spa,
                    'snn': snn,
                    'edad_actual': edad,
                    'ep': ep,
                    'cas': conductas,
                    'documento': documento,
                    'btnClass': "btn-success",
                    'btnText': "Guardar asesoría",
                    'secretName': "threeCapitor",
                    'spaActuales': spaActuales,
                })
            else:
                return render(request, 'sm_HPC.html', {
                    'CustomUser': request.user,
                    'step': 1,
                    'escolaridades': escolaridades,
                    'sexos': sexos,
                    'estados_civil': estados_civiles,
                    'lectoescrituras': lectoescritura1,
                    'lectoescritura_nivel': lectoescritura2,
                    'calculos': calculos,
                    'razonamiento_analitico': razonamiento,
                    'etnias': etnias,
                    'ocupaciones': ocupaciones,
                    'pips': pips,
                    'rsss': regimenes,
                    'epss': EPSS,
                    'year': datetime.now(),
                    'documento': documento,
                    'tipos_documento': tipos_documento,
                    'error': error
                })
        elif "detalles_asesoria" in request.POST:

            documento = request.POST['documento']
            id_profesional = request.POST['id_prof']
            edad_actual = request.POST['edad_actual']
            a_lugar = request.POST['a_lugar']
            ap_trans = request.POST['ap_trans']
            ap_cate = request.POST['ap_cate']
            ap_diag = request.POST['ap_diag']
            ap_trat = request.POST['ap_trat']
            ap_med = request.POST['ap_med']
            ap_adh = request.POST['ap_adh']
            ap_barr = request.POST['ap_barr']
            ap_notas = request.POST['ap_notas']
            sp_edad = request.POST['sp_edad']
            sp_susi = request.POST['sp_susi']  # i
            sp_ulco = request.POST['sp_ulco']  # f
            sp_susim = request.POST['sp_susim']  # i

            sp_csr = request.POST['sp_csr']
            sp_ip = request.POST['sp_ip']
            sp_vi = request.POST['sp_vi']
            sp_notas = request.POST['sp_notas']

            cs_pi = request.POST['cs_pi']  # i snn
            cs_pp = request.POST['cs_pp']  # i snn
            cs_dm = request.POST['cs_dm']  # i snn
            cs_ip = request.POST['cs_ip']
            cs_fu = request.POST['cs_fu']  # f
            cs_metodo = request.POST['cs_metodo']
            cs_let = request.POST['cs_let']
            cs_ss = request.POST['cs_ss']
            cs_eb = request.POST['cs_eb']  # i
            cs_ep = request.POST['cs_ep']  # i
            cs_ae = request.POST['cs_ae']
            cs_fp = request.POST['cs_fp']
            cs_ra = request.POST['cs_ra']
            cs_notas = request.POST['cs_notas']

            av_tv = request.POST['av_tv']
            av_agre = request.POST['av_agre']
            av_ir = request.POST['av_ir']
            av_notas = request.POST['av_notas']
            re_pt = request.POST['re_pt']
            re_cd = request.POST['re_cd']
            re_notas = request.POST['re_notas']
            seg_1 = request.POST['seg_1']
            seg_2 = request.POST['seg_2']
            
            try:
                pacienteInstance = InfoPacientes.objects.get(
                    documento=documento)
            except InfoPacientes.DoesNotExist:
                pacienteInstance = None

            try:
                id_profesionalInstance = InfoMiembros.objects.get(
                    id_usuario=id_profesional)
            except InfoMiembros.DoesNotExist:
                id_profesionalInstance = None

            try:
                spa_instance = SPA.objects.get(id=sp_susi)
            except SPA.DoesNotExist:
                spa_instance = None

            try:
                spa_instance2 = SPA.objects.get(id=sp_susim)
            except SPA.DoesNotExist:
                spa_instance2 = None

            if 'sp_cf' in request.POST:
                sp_cfins = True
            else:
                sp_cfins = False

            try:
                cs_fu = datetime.strptime(cs_fu, '%Y-%m-%d')
            except:
                cs_fu = None

            try:
                sp_ulco = datetime.strptime(sp_ulco, '%Y-%m-%d')
            except:
                sp_ulco = None

            try:
                cs_pins = SiNoNunca.objects.get(id=cs_pi)
            except SiNoNunca.DoesNotExist:
                cs_pins = None

            try:
                cs_ppins = SiNoNunca.objects.get(id=cs_pp)
            except SiNoNunca.DoesNotExist:
                cs_ppins = None

            try:
                cs_dmins = SiNoNunca.objects.get(id=cs_dm)
            except SiNoNunca.DoesNotExist:
                cs_dmins = None

            try:
                cs_ebins = SiNoNunca.objects.get(id=cs_eb)
            except SiNoNunca.DoesNotExist:
                cs_ebins = None

            try:
                cs_epins = EstatusPersona.objects.get(id=cs_ep)
            except EstatusPersona.DoesNotExist:
                cs_epins = None

            if 'sp_eoa' in request.POST:
                sp_eoa = True
            else:
                sp_eoa = False

            if 'cs_mh' in request.POST:
                cs_mh = True
            else:
                cs_mh = False

            if 'cs_hf' in request.POST:
                cs_hf = True
            else:
                cs_hf = False

            if 'av_vict' in request.POST:
                av_vict = True
            else:
                av_vict = False

            if 're_ac' in request.POST:
                re_ac = True
            else:
                re_ac = False

            if 're_sc' in request.POST:
                re_sc = True
            else:
                re_sc = False

            if 're_ic' in request.POST:
                re_ic = True
            else:
                re_ic = False

            if 're_io' in request.POST:
                re_io = True
            else:
                re_io = False
                
            if "secretKey" in request.POST:
                #actualizar la asesoría
                cita = request.GET.get('cita', 0)
                citaInstance = get_object_or_404(HPC, id=cita)
                
                try:
                    as_instance = HPC.objects.get(id=cita)
                except HPC.DoesNotExist:
                    as_instance = None
                print(f'tipo: {type(spa_instance)}')
                with transaction.atomic():
                    citaInstance.lugar = a_lugar
                    citaInstance.diag_trans_mental = ap_trans
                    citaInstance.diag_categoria=ap_cate
                    citaInstance.diag_por_profesional=ap_diag
                    citaInstance.tratamiento=ap_trat
                    citaInstance.medicamentos=ap_med
                    citaInstance.adherencia=ap_adh
                    citaInstance.barreras_acceso=ap_barr
                    citaInstance.anotaciones_antecedentes_psiquiatricos=ap_notas
                    citaInstance.es_hasido_consumidor=sp_eoa
                    citaInstance.edad_inicio=sp_edad
                    citaInstance.spa_inicio=spa_instance
                    citaInstance.sustancia_impacto=spa_instance2
                    citaInstance.periodo_ultimo_consumo=sp_ulco
                    citaInstance.conductas_sex_riesgo=sp_csr
                    citaInstance.intervenciones_previas=sp_ip
                    citaInstance.consumo_familiar=sp_cfins
                    citaInstance.vinculo=sp_vi
                    citaInstance.anotaciones_consumoSPA=sp_notas
                    citaInstance.tendencia_suicida=cs_pins
                    citaInstance.presencia_planeacion=cs_ppins
                    citaInstance.disponibilidad_medios=cs_dmins
                    citaInstance.intentos_previos=cs_ip
                    citaInstance.fecha_ultimo_intento=cs_fu
                    citaInstance.manejo_hospitalario=cs_mh
                    citaInstance.metodo=cs_metodo
                    citaInstance.letalidad=cs_let
                    citaInstance.signos=cs_ss
                    citaInstance.tratamiento_psiquiatrico=cs_ebins
                    citaInstance.estatus_persona=cs_epins
                    citaInstance.acontecimientos_estresantes=cs_ae
                    citaInstance.historial_familiar=cs_hf
                    citaInstance.factores_protectores=cs_fp
                    citaInstance.red_apoyo=cs_ra
                    citaInstance.anotaciones_comportamiento_suic=cs_notas
                    citaInstance.victima=av_vict
                    citaInstance.tipo_violencia=av_tv
                    citaInstance.agresor=av_agre
                    citaInstance.inst_reporte_legal=av_ir
                    citaInstance.anotaciones_antecedentes_violencia=av_notas
                    citaInstance.asistencia_cita=re_ac
                    citaInstance.contacto=re_sc
                    citaInstance.contacto_interrumpido=re_ic
                    citaInstance.inicia_otro_programa=re_io
                    citaInstance.p_tamizaje=re_pt
                    citaInstance.c_o_d=re_cd
                    citaInstance.anotaciones_libres_profesional=re_notas
                    citaInstance.seguimiento1=seg_1
                    citaInstance.seguimiento2=seg_2
                    citaInstance.save()
                    
                with transaction.atomic():
                    RHPCSituacionContacto.objects.filter(id_asesoria=cita).delete()
                    
                    for sit in hpcsituaciones:
                        checkbox_name = f'sit_{sit.id}'
                        if checkbox_name in request.POST:
                            try:
                                sitInstance = HPCSituacionContacto.objects.get(id=sit.id)
                            except HPCSituacionContacto.DoesNotExist:
                                sitInstance = None

                            situacion_contacto = RHPCSituacionContacto(
                                id_asesoria=as_instance,
                                id_situacion=sitInstance
                            )
                            situacion_contacto.save()
                            
                with transaction.atomic():
                    RHPCTiposDemandas.objects.filter(id_asesoria=cita).delete()
                    for dem in hpcdemandas:
                        checkbox_name = f'dem_{dem.id}'
                        if checkbox_name in request.POST:
                            try:
                                demInstance = HPCTiposDemandas.objects.get(id=dem.id)
                            except HPCTiposDemandas.DoesNotExist:
                                demInstance = None
                            demi = RHPCTiposDemandas(
                                id_asesoria=as_instance,
                                id_tipo_demanda=demInstance
                            )
                            demi.save()
                            
                with transaction.atomic():
                    RHPCTiposRespuestas.objects.filter(id_asesoria=cita).delete()
                    for tpr in hpcrespuestas:
                        checkbox_name = f'r_{tpr.id}'
                        if checkbox_name in request.POST:
                            try:
                                resInstance = HPCTiposRespuestas.objects.get(id=tpr.id)
                            except HPCTiposRespuestas.DoesNotExist:
                                resInstance = None
                            resTp = RHPCTiposRespuestas(
                                id_asesoria=as_instance,
                                id_respuesta=resInstance
                            )
                            resTp.save()
                
                with transaction.atomic():
                    RHPCConductasASeguir.objects.filter(id_asesoria=cita).delete()
                    for cs in conductas:
                        checkbox_name = f'cs_{cs.id}'
                        if checkbox_name in request.POST:
                            try:
                                conInstance = ConductasASeguir.objects.get(id=cs.id)
                            except ConductasASeguir.DoesNotExist:
                                conInstance = None
                            cond_s = RHPCConductasASeguir(
                                id_asesoria=as_instance,
                                id_conducta=conInstance
                            )
                            cond_s.save()
                            
                with transaction.atomic():
                    SPAActuales.objects.filter(id_paciente=documento).delete()
                    infoPacientesInstance = get_object_or_404(InfoPacientes, documento=documento)
                    for sp in spa:
                        checkbox_name = f'spac_{sp.id}'
                        if checkbox_name in request.POST:
                            try:
                                spa_instance = SPA.objects.get(id=sp.id)
                            except SPA.DoesNotExist:
                                spa_instance = None
                                
                            spact = SPAActuales(
                                id_paciente = infoPacientesInstance,
                                id_sustancia = spa_instance
                            )
                            spact.save()
                            
                return redirect(reverse('sm_historial_citas'))
            else:
                #Crear nueva asesoría
                
                asesoria = HPC(
                    cedula_usuario=pacienteInstance,
                    id_profesional=id_profesionalInstance,
                    lugar=a_lugar,
                    edad_usuario_actual=edad_actual,
                    diag_trans_mental=ap_trans,
                    diag_categoria=ap_cate,
                    diag_por_profesional=ap_diag,
                    tratamiento=ap_trat,
                    medicamentos=ap_med,
                    adherencia=ap_adh,
                    barreras_acceso=ap_barr,
                    anotaciones_antecedentes_psiquiatricos=ap_notas,
                    es_hasido_consumidor=sp_eoa,
                    edad_inicio=sp_edad,
                    spa_inicio=spa_instance,
                    sustancia_impacto=spa_instance2,
                    periodo_ultimo_consumo=sp_ulco,
                    conductas_sex_riesgo=sp_csr,
                    intervenciones_previas=sp_ip,
                    consumo_familiar=sp_cfins,
                    vinculo=sp_vi,
                    anotaciones_consumoSPA=sp_notas,
                    tendencia_suicida=cs_pins,
                    presencia_planeacion=cs_ppins,
                    disponibilidad_medios=cs_dmins,
                    intentos_previos=cs_ip,
                    fecha_ultimo_intento=cs_fu,
                    manejo_hospitalario=cs_mh,
                    metodo=cs_metodo,
                    letalidad=cs_let,
                    signos=cs_ss,
                    tratamiento_psiquiatrico=cs_ebins,
                    estatus_persona=cs_epins,
                    acontecimientos_estresantes=cs_ae,
                    historial_familiar=cs_hf,
                    factores_protectores=cs_fp,
                    red_apoyo=cs_ra,
                    anotaciones_comportamiento_suic=cs_notas,
                    victima=av_vict,
                    tipo_violencia=av_tv,
                    agresor=av_agre,
                    inst_reporte_legal=av_ir,
                    anotaciones_antecedentes_violencia=av_notas,
                    asistencia_cita=re_ac,
                    contacto=re_sc,
                    contacto_interrumpido=re_ic,
                    inicia_otro_programa=re_io,
                    p_tamizaje=re_pt,
                    c_o_d=re_cd,
                    anotaciones_libres_profesional=re_notas,
                    seguimiento1=seg_1,
                    seguimiento2=seg_2
                )
                asesoria.save()

                # Hacer el save y después generar el id
                id_asesoria = asesoria.id

                try:
                    as_instance = HPC.objects.get(id=id_asesoria)
                except HPC.DoesNotExist:
                    as_instance = None
                
                print(f'doc {documento}')
                with transaction.atomic():
                    SPAActuales.objects.filter(id_paciente=documento).delete()
                    infoPacientesInstance = get_object_or_404(InfoPacientes, documento=documento)
                    for sp in spa:
                        checkbox_name = f'spac_{sp.id}'
                        if checkbox_name in request.POST:
                            try:
                                spa_instance = SPA.objects.get(id=sp.id)
                            except SPA.DoesNotExist:
                                spa_instance = None
                                
                            spact = SPAActuales(
                                id_paciente = infoPacientesInstance,
                                id_sustancia = spa_instance
                            )
                            spact.save()

                for sit in hpcsituaciones:
                    checkbox_name = f'sit_{sit.id}'
                    if checkbox_name in request.POST:
                        try:
                            sitInstance = HPCSituacionContacto.objects.get(
                                id=sit.id)
                        except HPCSituacionContacto.DoesNotExist:
                            sitInstance = None

                        situacion_contacto = RHPCSituacionContacto(
                            id_asesoria=as_instance,
                            id_situacion=sitInstance
                        )
                        situacion_contacto.save()

                for dem in hpcdemandas:
                    checkbox_name = f'dem_{dem.id}'
                    if checkbox_name in request.POST:
                        try:
                            demInstance = HPCTiposDemandas.objects.get(id=dem.id)
                        except HPCTiposDemandas.DoesNotExist:
                            demInstance = None
                        demi = RHPCTiposDemandas(
                            id_asesoria=as_instance,
                            id_tipo_demanda=demInstance
                        )
                        demi.save()

                for tpr in hpcrespuestas:
                    checkbox_name = f'r_{tpr.id}'
                    if checkbox_name in request.POST:
                        try:
                            resInstance = HPCTiposRespuestas.objects.get(id=tpr.id)
                        except HPCTiposRespuestas.DoesNotExist:
                            resInstance = None
                        resTp = RHPCTiposRespuestas(
                            id_asesoria=as_instance,
                            id_respuesta=resInstance
                        )
                        resTp.save()

                for cs in conductas:
                    checkbox_name = f'cs_{cs.id}'
                    if checkbox_name in request.POST:
                        try:
                            conInstance = ConductasASeguir.objects.get(id=cs.id)
                        except ConductasASeguir.DoesNotExist:
                            conInstance = None
                        cond_s = RHPCConductasASeguir(
                            id_asesoria=as_instance,
                            id_conducta=conInstance
                        )
                        cond_s.save()

                return redirect(reverse('sm_historial_citas'))
    elif request.method == "GET":
        try:
            cita = request.GET.get('cita', 0)
            citaInfo = get_object_or_404(HPC, pk=cita)
            paciente = citaInfo.cedula_usuario_id

            if citaInfo.periodo_ultimo_consumo == None:
                citaInfo.periodo_ultimo_consumo = str("")
            else:
                citaInfo.periodo_ultimo_consumo = str(
                    citaInfo.periodo_ultimo_consumo)

            if citaInfo.fecha_ultimo_intento == None:
                citaInfo.fecha_ultimo_intento = str("")
            else:
                citaInfo.fecha_ultimo_intento = str(
                    citaInfo.fecha_ultimo_intento)

            situacionesContacto = RHPCSituacionContacto.objects.filter(
                id_asesoria_id=cita).values_list('id_situacion_id', flat=True)
            tiposDemandas = RHPCTiposDemandas.objects.filter(
                id_asesoria_id=cita).values_list('id_tipo_demanda_id', flat=True)
            respuestasCita = RHPCTiposRespuestas.objects.filter(
                id_asesoria_id=cita).values_list('id_respuesta_id', flat=True)
            conductasCita = RHPCConductasASeguir.objects.filter(
                id_asesoria_id=cita).values_list('id_conducta_id', flat=True)
            spaActuales = SPAActuales.objects.filter(
                id_paciente_id=paciente).values_list('id_sustancia_id', flat=True)

            return render(request, 'sm_HPC.html', {
                'CustomUser': request.user,
                'year': datetime.now(),
                'step': 2,
                'hpcsituaciones': hpcsituaciones,
                'hpcdemandas': hpcdemandas,
                'hpcrespuestas': hpcrespuestas,
                'spa': spa,
                'snn': snn,
                'fecha_nacimiento': fecha_nacimiento,
                'ep': ep,
                'cas': conductas,
                'data': citaInfo,
                'situacionesCita': situacionesContacto,
                'demandasCita': tiposDemandas,
                'respuestasCita': respuestasCita,
                'conductasCita': conductasCita,
                'spaActuales': spaActuales,
                'btnClass': "btn-warning",
                'btnText': "Actualizar asesoría",
                'secretName': "secretKey",
                'documento': paciente
            })
        except:
            return render(request, 'sm_HPC.html', {
                'CustomUser': request.user,
                'step': 0
            })
    else:
        return render(request, 'sm_HPC.html', {
            'CustomUser': request.user,
            'step': 0
        })
    try:
        return render(request, 'sm_HPC.html', {
            'CustomUser': request.user,
            'paciente': paciente,
            'year': datetime.now(),
            'step': 0
        })
    except:
        return render(request, 'sm_HPC.html', {
            'CustomUser': request.user,
            'year': datetime.now(),
            'step': 0
        })


@login_required
def sm_historial_llamadas(request):
    llamadas = PsiLlamadas.objects.all().order_by('-fecha_llamada')
    form = FiltroLlamadasForm(request.GET)
    
    #sistema de filtrado
    if form.is_valid():
        id_llamada = form.cleaned_data.get('id_llamada')
        id_profesional = form.cleaned_data.get('id_profesional')
        documento_paciente = form.cleaned_data.get('documento_paciente')
        fecha_llamada = form.cleaned_data.get('fecha_llamada')
        solo_hechas_por_mi = form.cleaned_data.get('solo_hechas_por_mi')
        
        if id_llamada:
            llamadas = llamadas.filter(id=id_llamada)
        if id_profesional:
            llamadas = llamadas.filter(Q(id_psicologo_id=Cast(Value(id_profesional), CharField())) | Q(id_psicologo_id=None))
        if documento_paciente:
            llamadas = llamadas.filter(documento=documento_paciente)
        if fecha_llamada:
            llamadas = llamadas.filter(fecha_llamada__date=fecha_llamada)
        if solo_hechas_por_mi:
            user_id = str(request.user.id)
            llamadas = llamadas.filter(
                Q(id_psicologo_id=Cast(Value(user_id), CharField())) | Q(id_psicologo_id=None)
            )
    
    # Paginación
    llamadas_por_pagina = 10
    paginator = Paginator(llamadas, llamadas_por_pagina)
    page = request.GET.get('page', 1)
    
    try:
        llamadas = paginator.page(page)
    except EmptyPage:
        llamadas = paginator.page(paginator.num_pages)
    
    return render(request, 'sm_historial_llamadas.html',{
        'CustomUser': request.user,
        'year': datetime.now(),
        'form': form,
        'llamadas': llamadas,
    })

@login_required
def sm_historial_citas(request):
    citas_with_pacientes = HPC.objects.select_related('cedula_usuario').order_by('-fecha_asesoria')
    citas_por_pagina = 10
    # Sistema de filtrado
    form = FiltroCitasForm(request.GET)
    if form.is_valid():  
        id_cita = form.cleaned_data.get('id_cita')
        id_profesional = form.cleaned_data.get('id_profesional')
        documento_paciente = form.cleaned_data.get('documento_paciente')
        fecha_cita = form.cleaned_data.get('fecha_cita')
        solo_hechas_por_mi = form.cleaned_data.get('solo_hechas_por_mi')

        if id_cita:
            citas_with_pacientes = citas_with_pacientes.filter(id=id_cita)
        if id_profesional:
            citas_with_pacientes = citas_with_pacientes.filter(Q(id_profesional_id=Cast(Value(id_profesional), CharField())) | Q(id_profesional_id=None))
        if documento_paciente:
            citas_with_pacientes = citas_with_pacientes.filter(cedula_usuario__documento=documento_paciente)
        if fecha_cita:
            citas_with_pacientes = citas_with_pacientes.filter(fecha_asesoria__date=fecha_cita)
        if solo_hechas_por_mi:
            user_id = str(request.user.id)
            citas_with_pacientes = citas_with_pacientes.filter(
                Q(id_profesional_id=Cast(Value(user_id), CharField())) | Q(id_profesional_id=None)
            )

    # Paginación
    
    paginator = Paginator(citas_with_pacientes, citas_por_pagina)
    page = request.GET.get('page', 1)

    try:
        citas = paginator.page(page)
    except EmptyPage:
        citas = paginator.page(paginator.num_pages)

    return render(request, 'sm_historial_citas.html', {
        'CustomUser': request.user,
        'year': datetime.now(),
        'citas': citas,
        'form': form
    })




# Admin
@login_required
def detallesusuario(request):
    # Super Proteger Ruta
    if request.user.tipo_usuario_id in adminOnly:
        userToBrowse = request.GET.get('userId', 0)  
        
        if request.method == "POST": 
            
            if "emergencyChange" in request.POST:
                return redirect(reverse('adminuser'))
            else:
                #InfoMiembros
                nombre = request.POST['nombre']
                documento = request.POST['documento']
                tipo_documento = request.POST['tipo_documento'] #i
                numHijos = request.POST['numHijos']
                barrio = request.POST['barrio']
                direccion = request.POST['direccion']
                celular = request.POST['celular']
                eps = request.POST['eps'] #i
                estadoCivil = request.POST['estadoCivil'] #i
                etnia = request.POST['etnia'] #i
                regimen = request.POST['regimen'] #i
                sexo = request.POST['sexo'] #i
                #Account Customuser
                username = request.POST['username']
                email = request.POST['email']
                
                
                
                if "sisben" in request.POST:
                    sisben = True
                else:
                    sisben = False
                
                try:
                    infoMiembro = InfoMiembros.objects.filter(id_usuario_id=userToBrowse).first()
                except InfoMiembros.DoesNotExist:
                    infoMiembro = None
                
                try:
                    custoMuserInstance = CustomUser.objects.filter(id=userToBrowse).first()
                except CustomUser.DoesNotExist:
                    custoMuserInstance = None
                    
                if infoMiembro and custoMuserInstance:
                    #Actualizar datos personales del usuario
                    infoMiembro.nombre = nombre if nombre else infoMiembro.nombre
                    
                    try:
                        verifyDoc = InfoMiembros.objects.filter(documento=documento).first()
                    except InfoMiembros.DoesNotExist:
                        verifyDoc = None
                    except:
                        verifyDoc = None
                        
                    #Instances
                    try:
                        tpDocumentoInstance = TipoDocumento.objects.get(id=tipo_documento)
                    except TipoDocumento.DoesNotExist:
                        tpDocumentoInstance = None
                    
                    try:
                        epsInstance = EPS.objects.get(id=eps)
                    except EPS.DoesNotExist:
                        epsInstance= None
                        
                    try:
                        esCivilInstance = EstadoCivil.objects.get(id=estadoCivil)
                    except EstadoCivil.DoesNotExist:
                        esCivilInstance = None
                        
                    try:
                        etniaInstance = Etnia.objects.get(id=etnia)
                    except Etnia.DoesNotExist:
                        etniaInstance = None
                        
                    try:
                        regInstace = RegimenSeguridad.objects.get(id=regimen)
                    except RegimenSeguridad.DoesNotExist:
                        regInstace = None
                        
                    try:
                        sexoInstance = Sexo.objects.get(id=sexo)
                    except Sexo.DoesNotExist:
                        sexoInstance = None
                        
                    
                    infoMiembro.documento = documento if verifyDoc == None else infoMiembro.documento
                    infoMiembro.direccion = direccion if direccion else infoMiembro.direccion
                    infoMiembro.barrio = barrio if barrio else infoMiembro.barrio
                    infoMiembro.celular = celular if celular else infoMiembro.celular
                    infoMiembro.numero_hijos = numHijos if numHijos else infoMiembro.numero_hijos
                    infoMiembro.tipo_documento = tpDocumentoInstance if tpDocumentoInstance else infoMiembro.tipo_documento
                    infoMiembro.eps = epsInstance if epsInstance else infoMiembro.eps
                    infoMiembro.estado_civil = esCivilInstance if esCivilInstance else infoMiembro.estado_civil
                    infoMiembro.etnia = etniaInstance if etniaInstance else infoMiembro.etnia
                    infoMiembro.regimen_seguridad = regInstace if regInstace else infoMiembro.regimen_seguridad
                    infoMiembro.sexo = sexoInstance if sexoInstance else infoMiembro.sexo
                    infoMiembro.sisben = sisben
                    
                    infoMiembro.save()
                    
                    #actualizar datos de la cuenta del usuario
                    custoMuserInstance.username = username if username else custoMuserInstance.username
                    custoMuserInstance.email = email if email else custoMuserInstance.email
                    
                    custoMuserInstance.save()
                    
                    
                return redirect(reverse('adminuser'))
        else:
            if userToBrowse and userToBrowse != 0:
                userInstance = InfoMiembros.objects.select_related('id_usuario').get(id_usuario=userToBrowse)
                editable = request.GET.get('editable', 0)
                
                if not editable or editable == 0:
                    return render(request, 'userDetails.html', {
                    'CustomUser': request.user,
                    'year': datetime.now(),
                    'userI':userInstance,
                    'tiposDoc':tipos_documento,
                    'estadosC': estados_civiles,
                    'sexos': sexos,
                    'etnias': etnias,
                    'regimenes': regimenes,
                    'eps': EPSS, 
                    'btnClass': "btn btn-primary",
                    'btnText': 'Volver',})
                else:
                    return render(request, 'userDetails.html', {
                    'CustomUser': request.user,
                    'year': datetime.now(),
                    'userI':userInstance,
                    'tiposDoc':tipos_documento,
                    'estadosC': estados_civiles,
                    'sexos': sexos,
                    'etnias': etnias,
                    'regimenes': regimenes,
                    'eps': EPSS,
                    'editable': editable,
                    'btnClass': "btn btn-warning",
                    'btnText': 'Actualizar usuario',})
            else:
                return redirect(reverse('adminuser'))
    else:
        return redirect(reverse('home'))

@login_required
def eventHandler(request):
    if request.method == "GET":
        event = request.GET.get('eventId', 0)
        userId = request.GET.get('userId', 0)
        custoMuserInstance = get_object_or_404(CustomUser,pk=userId)
        #banear
        if event == "1" and custoMuserInstance:
            custoMuserInstance.is_active = False
            custoMuserInstance.save()
        #desbanear
        elif event == "2" and custoMuserInstance:
            custoMuserInstance.is_active = True
            custoMuserInstance.save()
        #borrar usuario
        elif event == "3" and custoMuserInstance:
            #borrar
            if custoMuserInstance:
                # Borra el usuario
                custoMuserInstance.delete()
        #cambiar contraseña
        elif event == "4" and custoMuserInstance:    
            nuevaContrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8,12)))
            custoMuserInstance.set_password(nuevaContrasena)
            custoMuserInstance.save()
            print(nuevaContrasena)
            
            return render(request, 'userDetails.html', {
                    'CustomUser': request.user,
                    'year': datetime.now(),
                    'userI':custoMuserInstance,
                    'tiposDoc':tipos_documento,
                    'estadosC': estados_civiles,
                    'sexos': sexos,
                    'etnias': etnias,
                    'regimenes': regimenes,
                    'eps': EPSS,
                    'editable': True,
                    'btnClass': "btn btn-warning",
                    'btnText': 'Actualizar usuario',
                    'passMsg': f"Se ha actualizado correctamente. Por favor notifique a {custoMuserInstance.username}. Nueva contraseña: {nuevaContrasena}"})
        else:
            pass
        
        return redirect(reverse('adminuser'))
    else:
        return redirect(reverse('adminuser'))
    
    CBjwelZtyu
@login_required
def adminuser(request):
    # Super Proteger Ruta
    if request.user.tipo_usuario_id in adminOnly:
        users = InfoMiembros.objects.all()
        form = FiltroUsuarios(request.GET)  # Instancia del formulario
        usuarios_por_pagina = 10
        

        #Filtrado
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            id_usuario = form.cleaned_data.get('id_usuario')
            documento_usuario = form.cleaned_data.get('documento_usuario')
            
            if nombre:
                normalized_term = unidecode(nombre.lower())
                users = users.extra(where=["unaccent(lower(nombre)) ILIKE unaccent(%s)"], params=['%' + normalized_term + '%'])

            if id_usuario:
                users = users.filter(id_usuario=id_usuario)
            if documento_usuario:
                users = users.filter(documento=documento_usuario)
        
        #paginación
        paginator = Paginator(users, usuarios_por_pagina)
        page = request.GET.get('page', 1)
        
        try:
            users = paginator.page(page)
        except:
            users = paginator.page(page)
        
        return render(request, 'AdminUser.html', {
            'CustomUser': request.user,
            'year': datetime.now(),
            'users': users,
            'form': form
        })
    else:
        return redirect(reverse('home'))


@login_required
def adminregister(request):
    #Super Proteger Ruta
    if request.user.tipo_usuario_id in adminOnly:
        return render(request, 'AdminRegister.html',{
            'CustomUser': request.user,
            'year': datetime.now(),
        })
    else:
        return redirect(reverse('home'))
    
# 404 VISTAS
@login_required
def restricted_area_404(request):
    if request.method == "GET":
        return render(request, '404_restricted_area.html')


@login_required
def not_deployed_404(request):
    if request.method == "GET":
        return render(request, '404_not_deployed.html')



