from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserRegistrationForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import IntegrityError, transaction
from .forms import TrabajadorEditForm, AdministradorEditForm, AutodataForm
from .models import SiNoNunca, CustomUser, EstadoCivil, InfoMiembros, InfoPacientes, Pais, Departamento, Municipio, TipoDocumento, Sexo, EPS, PoblacionVulnerable, PsiMotivos, ConductasASeguir, PsiLlamadas, PsiLlamadasConductas, PsiLlamadasMotivos, Escolaridad, Lecto1, Lecto2, Calculo, PacienteCalculo, Razonamiento, Etnia, Ocupacion, Pip, PacientePip, RegimenSeguridad, HPCSituacionContacto, HPCTiposDemandas, HPCTiposRespuestas, SPA
from django.http import JsonResponse
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


# Create your views here.

@login_required
def sm_llamadas(request):
    if request.method == "POST":
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
        
        try:
            sexo_instance = Sexo.objects.get(id=sexo)
        except Sexo.DoesNotExist:
            # Manejar el caso donde no se encontró una instancia de Sexo
            sexo_instance = None
    
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
            sexo = sexo_instance,
            edad = edad
        )
        llamada.save()
        id_llamada = llamada.id
        
        try:
            psi_llamada_instance = PsiLlamadas.objects.get(id=id_llamada)
        except PsiLlamadas.DoesNotExist:
            psi_llamada_instance = None
            
        ##conductas y motivos
        for conducta in ConductasASeguir.objects.all():
            checkbox_name = f'cond_{conducta.id}'
            if checkbox_name in request.POST:
                try:
                    conducta_instance = ConductasASeguir.objects.get(id=conducta.id)
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
                    motivo_instace = PsiMotivos.objects.get(id=motivo.id)
                except PsiMotivos.DoesNotExist:
                    motivo_instace = None
                
                llamada_motivo = PsiLlamadasMotivos(
                    id_llamada=psi_llamada_instance,
                    id_motivo=motivo_instace
                )
                llamada_motivo.save()

        ##paciente
        paciente_existe = InfoPacientes.objects.filter(documento = documento).first()

        try:
            tipo_documento_instance = TipoDocumento.objects.get(id=tipo_documento)
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
            pob_vulnerable_instance = PoblacionVulnerable.objects.get(id=pob_vulnerable)
        except PoblacionVulnerable.DoesNotExist:
            pob_vulnerable_instance = None    
        
        if paciente_existe:
            #Si el paciente existe se actualizan los datos
            paciente_existe.nombre = nombre.lower()
            paciente_existe.tipo_documento = tipo_documento_instance
            
            paciente_existe.sexo = sexo_instance
            paciente_existe.edad = edad
            paciente_existe.eps = eps_instance
            paciente_existe.direccion = direccion.lower()
            paciente_existe.municipio = municipio_instance
            paciente_existe.poblacion_vulnerable = pob_vulnerable_instance
            paciente_existe.celular = telefono
            paciente_existe.save()
        else:
            ##Si no existe, se crea un paciente nuevo
            nuevo_paciente = InfoPacientes(
                nombre=nombre.lower(),
                documento = documento,
                tipo_documento = tipo_documento_instance,
                sexo = sexo_instance,
                edad = edad,
                eps = eps_instance,
                direccion = direccion.lower(),
                municipio = municipio_instance,
                poblacion_vulnerable = pob_vulnerable_instance,
                celular = telefono
            )
            nuevo_paciente.save()
            
            # select * from main_infopacientes
            # select * from main_psillamadasconductas
            # select * from main_psillamadasmotivos
            # select * from main_psillamadas

            # delete from main_psillamadas;
            # delete from main_psillamadasmotivos;
            # delete from main_psillamadasconductas;
            # delete from main_infopacientes;
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

def get_departamentos(request):
    pais_id = request.GET.get('pais_id')
    if pais_id:
        try:
            pais = get_object_or_404(Pais, id=pais_id)
            departamentos = Departamento.objects.filter(pertenece_pais_id=pais)
            data = [{'id': departamento.id, 'description': departamento.description} for departamento in departamentos]
            return JsonResponse(data, safe=False)
        except Pais.DoesNotExist:
            return JsonResponse([], safe=False)

    return JsonResponse([], safe=False)

def get_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    if departamento_id:
        try:
            departamento = get_object_or_404(Departamento, id=departamento_id)
            municipios = Municipio.objects.filter(pertenece_departamento_id=departamento)
            data = [{'id': municipio.id, 'description': municipio.description} for municipio in municipios]
            return JsonResponse(data, safe=False)
        except Departamento.DoesNotExist:
            return JsonResponse([], safe=False)

    return JsonResponse([], safe=False)
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
    documento = ""
    if request.method == "POST":
        if "comprobar_documento" in request.POST:
            documento = request.POST['documento']
            try:
                paciente = InfoPacientes.objects.get(documento=documento)
            except InfoPacientes.DoesNotExist:
                paciente = None
            return render(request, 'sm_HPC.html',{
                'CustomUser': request.user,
                'paciente': paciente,
                'step' : 1,
                'escolaridades':escolaridades,
                'sexos': sexos,
                'estados_civil':estados_civiles,
                'lectoescrituras':lectoescritura1,
                'lectoescritura_nivel': lectoescritura2,
                'calculos':calculos,
                'razonamiento_analitico':razonamiento,
                'etnias':etnias,
                'ocupaciones':ocupaciones,
                'pips': pips,
                'rsss':regimenes,
                'epss':EPSS,
                'year': datetime.now(),
                'documento': documento,
                'tipos_documento':tipos_documento
            })
        elif "actualizar_usuario" in request.POST:
            try:
                documento = request.POST['e_documento']
                print(documento)
                paciente = get_object_or_404(InfoPacientes, documento=documento)

                nombre = request.POST['e_nombre']
                tipo_documento = request.POST['e_tipo_documento']
                fecha_nacimiento = request.POST['e_fecha_nacimiento']
                edad = request.POST['e_edad']
                escolaridad = request.POST['e_escolaridad']
                numero_hijos = request.POST['e_hijos']
                sexo = request.POST['e_sexo']
                direccion = request.POST['e_direccion']
                barrio = request.POST['e_barrio']
                estado_civil = request.POST['e_estado_civil']
                celular = request.POST['e_celular']
                correo = request.POST['e_correo']
                lectoescritura = request.POST['e_lect']
                lect_nivel = request.POST['e_lect2']
                raz_analitico = request.POST['e_raz_analitico']
                etnia = request.POST['e_etnia']
                ocupacion = request.POST['e_ocupacion']
                regimen = request.POST['e_rss']

                # Validación simplificada de sisben
                sisben = request.POST.get('e_sisben') == 'on'

                # Instancias simplificadas usando get_object_or_404
                tipo_documento_instance = get_object_or_404(TipoDocumento, id=tipo_documento)
                escolaridad_instance = get_object_or_404(Escolaridad, id=escolaridad)
                sexo_instance = get_object_or_404(Sexo, id=sexo)
                estado_civil_instance = get_object_or_404(EstadoCivil, id=estado_civil)
                lecto1_instance = get_object_or_404(Lecto1, id=lectoescritura)
                lecto2_instance = get_object_or_404(Lecto2, id=lect_nivel)
                razonamiento_instance = get_object_or_404(Razonamiento, id=raz_analitico)
                etnia_instance = get_object_or_404(Etnia, id=etnia)
                ocupacion_instance = get_object_or_404(Ocupacion, id=ocupacion)
                regimen_seguridad_instance = get_object_or_404(RegimenSeguridad, id=regimen)
                eps_instance = get_object_or_404(EPS, id=request.POST['eps'])

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

            except (TipoDocumento.DoesNotExist, Escolaridad.DoesNotExist, Sexo.DoesNotExist, EstadoCivil.DoesNotExist, Lecto1.DoesNotExist, Lecto2.DoesNotExist, Razonamiento.DoesNotExist, Etnia.DoesNotExist, Ocupacion.DoesNotExist, RegimenSeguridad.DoesNotExist, EPS.DoesNotExist):
                # Manejar excepciones específicas según sea necesario
                # Puedes agregar un manejo de errores más específico aquí
                pass

            # Redirigir a una página de detalles del paciente u otra vista después de la actualización
            return render(request, 'sm_HPC.html',{
                'CustomUser': request.user,
                'year': datetime.now(),
                'step': 2,
                'hpcsituaciones': hpcsituaciones,
                'hpcdemandas':hpcdemandas,
                'hpcrespuestas': hpcrespuestas,
                'spa': spa,
                'snn': snn
                
            })           
        elif "crear_usuario" in request.POST:      
            nombre = f"{request.POST['nombre']} {request.POST['apellido']}"
            documento = request.POST.get('documento_bait', None)
            if not documento:
                documento = request.POST.get('documento', None)
            documento = request.POST['documento']
            tipo_documento = request.POST['tipo_documento']
            sexo = request.POST['sexo']
            edad = request.POST['edad']
            eps = request.POST['eps']
            direccion = request.POST['direccion']
            celular = request.POST['celular']
            fecha_nacimiento = request.POST['fecha_nacimiento']
            escolaridad = request.POST['escolaridad']
            hijos = request.POST['hijos']
            barrio = request.POST['barrio']
            estado_civil= request.POST['estado_civil']
            correo = request.POST['correo']
            lectoescritura = request.POST['lectoescritura']
            raz_analitico = request.POST['raz_analitico']
            lect_nivel = request.POST['lect_nivel']
            ocupacion = request.POST['ocupacion']
            regimen = request.POST['rss']
            if 'sisben' in request.POST:
                sisben = True
            else:
                sisben = False
            eps = request.POST['eps']
            etnia = request.POST['etnia']
            
                
            #INSTANCIAS
            # try:
            #     paciente = InfoPacientes.objects.get(documento=documento)
            # except InfoPacientes.DoesNotExist:
            #     paciente = None
            
            try:
                tipo_documento_instance = TipoDocumento.objects.get(id=tipo_documento)
            except TipoDocumento.DoesNotExist:
                tipo_documento_instance = None
            
            try:
                escolaridad_instance  = Escolaridad.objects.get(id=escolaridad)
            except Escolaridad.DoesNotExist:
                escolaridad_instance = None
                
            try:
                sexo_instance = Sexo.objects.get(id=sexo)
            except Sexo.DoesNotExist:
                sexo_instance = None
                
            try:
                estado_civil_instance = EstadoCivil.objects.get(id=estado_civil)
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
                razonamiento_instance = Razonamiento.objects.get(id=raz_analitico)
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
                regimen_seguridad_instance = RegimenSeguridad.objects.get(id=regimen)
            except:
                regimen_seguridad_instance = None
                
            try:
                eps_instance = EPS.objects.get(id=eps)
            except EPS.DoesNotExist:
                eps_instance = None
            
            nuevo_usuario = InfoPacientes(
                nombre = nombre,
                documento = documento,
                tipo_documento = tipo_documento_instance,
                fecha_nacimiento = fecha_nacimiento,
                edad = edad,
                escolaridad = escolaridad_instance,
                numero_hijos = hijos,
                sexo = sexo_instance,
                direccion = direccion,
                barrio = barrio,
                estado_civil = estado_civil_instance,
                celular = celular,
                email = correo,
                lectoescritura_indicador = lecto1_instance,
                lectoescritura_nivel = lecto2_instance,
                razonamiento_analitico =razonamiento_instance,
                etnia = etnia_instance,
                ocupacion = ocupacion_instance,
                regimen_seguridad = regimen_seguridad_instance,
                eps = eps_instance,
                sisben = sisben
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
                        documento_usuario = nuevo_usuario,
                        id_calculo = calculo_instance
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
                        documento_usuario = nuevo_usuario,
                        id_pip = pip_instance
                    )
                    pp.save()
                    
            return render(request, 'sm_HPC.html',{
                'CustomUser': request.user,
                'year': datetime.now(),
                'step': 2
            })
        elif "detalles_asesoria" in request.POST:
            lugar = request.POST['a_lugar']
            transtorno = request.POST['ap_trans']
            categoria_trans = request.POST['ap_cate']
            tratamiento = request.POST['ap_trat']
            medicamentos = request.POST['ap_med']
            adherencia = request.POST['ap_adh']
            barreras = request.POST['ap_barr']
            notas_ap = request.POST['ap_notas'] 
            eoha = request.POST['sp_eoa']
            edad_inicio = request.POST['sp_edad']
            spa_inicio = request.POST['sp_susi'] #i
            periodo_uc = request.POST['sp_ulco']
            spa_impacto = request.POST['sp_susim'] #i
            cond_s_riesgo = request.POST['sp_csr']
            int_previas = request.POST['sp_ip']
            cons_familiar = request.POST['sp_cf']
            vinculo = request.POST['sp_vi']
            notas_sp = request.POST['sp_notas']
            presencia = request.POST['cs_pi'] #i snn
            p_planeacion = request.POST['cs_pp'] #i snn
            disp_medios = request.POST['cs_dm'] #i snn
            int_previos = request.POST['cs_ip']
            fech_ulin = request.POST['cs_fu']
            man_hosp = request.POST['cs_mh']
            metodo = request.POST['cs_dm'] #i metodos
            letalidad = request.POST['cs_let']
            sig_sint = request.POST['cs_ss']
                        
            
            
            
            
            
    
    else:
        return render(request, 'sm_HPC.html',{
        'CustomUser': request.user,
        'step': 0
    })
        
    return render(request, 'sm_HPC.html',{
        'CustomUser': request.user,
        'paciente': paciente,
        'year': datetime.now(),
    })
    
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