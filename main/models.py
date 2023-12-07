from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.utils import timezone
import datetime

# Create your models here.
""" 
########### AUTH MODELS ###########
El modelo CustomUser es usado para iniciar la sesión en el navegador.
CustomUserManager es un handler que ayuda a la creación de un nuevo usuario que puede iniciar sesión.
"""
# Tabla foránea


class TipoUsuario(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo de nombre de usuario es obligatorio')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Los superusuarios deben tener is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_set')
    tipo_usuario = models.ForeignKey(
        TipoUsuario, on_delete=models.DO_NOTHING, default=3)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super(CustomUser, self).save(*args, **kwargs)

    """ 
###### MODELOS FORÁNEOS GENERALES 1 a 1 ######
Para normalizar la base de datos.
Algunos vienen con información preestablecida
"""


class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Escolaridad(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Sexo(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class EstadoCivil(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Lecto1(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Lecto2(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Razonamiento(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Etnia(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Ocupacion(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class RegimenSeguridad(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Calculo(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Pip(models.Model):  # POBLACION IDENTIFICADA POR PARTICULARIDADES
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class PoblacionVulnerable(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Pais(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description.capitalize()


class Departamento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    pertenece_pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.description.capitalize()


class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    pertenece_departamento = models.ForeignKey(
        Departamento, on_delete=models.DO_NOTHING)
    guardado_por = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.description.capitalize()


class DiaNombre(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=15)

    def __str__(self):
        return self.description.capitalize()


class HPCSituacionContacto(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class HPCTiposDemandas(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class HPCTiposRespuestas(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class SPA(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class HPCMetodosSuicida(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class EstatusPersona(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class SiNoNunca(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description.capitalize()


class ConductasASeguir(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=80)

    def __str__(self):
        return self.description.capitalize()


class PsiMotivos(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=80)

    def __str__(self):
        return self.description.capitalize()


class EPS(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=80)

    def __str__(self):
        return self.description.capitalize()


""" 
##### MODELO DE INFORMACIÓN PARA USUARIOS #####
En este modelo se guarda la información general de los usuarios que acuden
personalmente a asesorías. Cumple la función de la primer hoja del HPC.
Si hay un usuario que volvió a asistir a la asesoría y ya diligenció este formulario,
se le notificará al psicologo y le mostrará el formulario con los datos recolectados anteriormente,
el objetivo es que el psicologo confirme la información del usuario y la actualice si es necesario.
"""


class InfoPacientes(models.Model):
    documento = models.CharField(primary_key=True, max_length=20, null=False)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    nombre = models.TextField(max_length=200)
    email = models.EmailField(max_length=254)
    fecha_nacimiento = models.DateField(null=True)
    escolaridad = models.ForeignKey(
        Escolaridad, on_delete=models.CASCADE, null=True)
    numero_hijos = models.IntegerField(null=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE)
    direccion = models.TextField(max_length=150, null=True)
    edad = models.IntegerField(null=True, blank=True)
    municipio = models.ForeignKey(
        Municipio, on_delete=models.CASCADE, null=True, blank=True)
    barrio = models.CharField(max_length=100, null=True)
    poblacion_vulnerable = models.ForeignKey(
        PoblacionVulnerable, null=True, on_delete=models.CASCADE)
    estado_civil = models.ForeignKey(
        EstadoCivil, on_delete=models.CASCADE, null=True)
    celular = models.CharField(null=True)
    lectoescritura_indicador = models.ForeignKey(
        Lecto1, on_delete=models.CASCADE, null=True)
    lectoescritura_nivel = models.ForeignKey(
        Lecto2, on_delete=models.CASCADE, null=True)
    razonamiento_analitico = models.ForeignKey(
        Razonamiento, on_delete=models.CASCADE, null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.CASCADE, null=True)
    ocupacion = models.ForeignKey(
        Ocupacion, on_delete=models.CASCADE, null=True)
    regimen_seguridad = models.ForeignKey(
        RegimenSeguridad, on_delete=models.CASCADE, null=True)
    sisben = models.BooleanField(null=True)
    eps = models.ForeignKey(EPS, on_delete=models.CASCADE, null=True)
    cant_asesorias_psicologicas = models.IntegerField(default=0)
    cant_llamadas = models.IntegerField(default=0)

# Rompimientos


class PacienteCalculo(models.Model):
    documento_usuario = models.ForeignKey(
        InfoPacientes, on_delete=models.DO_NOTHING)
    id_calculo = models.ForeignKey(Calculo, on_delete=models.DO_NOTHING)


class PacientePip(models.Model):
    documento_usuario = models.ForeignKey(
        InfoPacientes, on_delete=models.DO_NOTHING)
    id_pip = models.ForeignKey(Pip, on_delete=models.DO_NOTHING)


"""
##### MODELO DE INFORMACIÓN PARA TRABAJADORES #####
En este modelo se guarda la información de los trabajadores, es similar al de los pacientes
sólo que con algunos campos menos que se consideraron innecesarios.
"""


class InfoMiembros(models.Model):
    documento = models.CharField(max_length=20, null=False)
    nombre = models.CharField(max_length=150, null=True)
    tipo_documento = models.ForeignKey(
        TipoDocumento, on_delete=models.DO_NOTHING, null=True)
    id_usuario = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    numero_hijos = models.IntegerField(null=False, default=0)
    sexo = models.ForeignKey(Sexo, on_delete=models.DO_NOTHING, null=True)
    direccion = models.CharField(max_length=100, null=False)
    barrio = models.CharField(max_length=100, null=False)
    estado_civil = models.ForeignKey(
        EstadoCivil, on_delete=models.DO_NOTHING, null=True)
    celular = models.CharField(null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.DO_NOTHING, null=True)
    regimen_seguridad = models.ForeignKey(
        RegimenSeguridad, on_delete=models.DO_NOTHING, null=True)
    sisben = models.BooleanField(null=True, default=False)
    nombre_eps = models.CharField(max_length=50)
    contador_llamadas_psicologicas = models.IntegerField(
        null=False, default=0)  # tr
    contador_asesorias_psicologicas = models.IntegerField(
        null=False, default=0)  # tr

    def __str__(self):
            return str(self.id_usuario)

"""
##### MODELO DE INFORMACIÓN DE LLAMADAS #####
Aquí se guarda la información proveniente de las llamadas psicologicas.
"""


class PsiLlamadas(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.CharField(max_length=30, null=True, blank=True)
    nombre_paciente = models.CharField(null=True, max_length=100)
    id_psicologo = models.ForeignKey(InfoMiembros, on_delete=models.DO_NOTHING)
    fecha_llamada = models.DateTimeField(default=timezone.now)
    dia_semana = models.ForeignKey(DiaNombre, on_delete=models.PROTECT)
    sexo = models.ForeignKey(Sexo, null=True, on_delete=models.CASCADE)
    edad = models.IntegerField(null=True)
    observaciones = models.TextField(null=True, max_length=5000)
    seguimiento24 = models.TextField(null=True, max_length=5000)
    seguimiento48 = models.TextField(null=True, max_length=5000)
    seguimiento72 = models.TextField(null=True, max_length=5000)

# Rompimientos


class PsiLlamadasConductas(models.Model):
    id_llamada = models.ForeignKey(PsiLlamadas, on_delete=models.CASCADE)
    id_conducta = models.ForeignKey(ConductasASeguir, on_delete=models.CASCADE)


class PsiLlamadasMotivos(models.Model):
    id_llamada = models.ForeignKey(PsiLlamadas, on_delete=models.CASCADE)
    id_motivo = models.ForeignKey(PsiMotivos, on_delete=models.CASCADE)


""" 
##### MODELO HPC #####
En este modelo se recolectará la información proveniente de la hoja de primer contacto HPC
"""


class HPC(models.Model):
    id = models.AutoField(primary_key=True)
    cedula_usuario = models.ForeignKey(
        InfoPacientes, on_delete=models.DO_NOTHING)
    id_profesional = models.ForeignKey(
        InfoMiembros, on_delete=models.DO_NOTHING, to_field='id_usuario')
    fecha_asesoria = models.DateTimeField(default=timezone.now)
    lugar = models.TextField(max_length=150, null=True)
    edad_usuario_actual = models.IntegerField(null=True)
    diag_trans_mental = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    diag_categoria = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    diag_por_profesional = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    tratamiento = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    medicamentos = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    adherencia = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    barreras_acceso = models.TextField(
        max_length=300, null=True, default=models.SET_NULL)
    es_hasido_consumidor = models.BooleanField(default=False)
    edad_inicio = models.IntegerField(null=True, default=models.SET_NULL)
    spa_inicio = models.ForeignKey(
        SPA, null=True, on_delete=models.DO_NOTHING, related_name='hpc_spa_inicio')
    sustancia_impacto = models.ForeignKey(
        SPA, null=True, on_delete=models.DO_NOTHING, related_name='hpc_sustancia_impacto')
    periodo_ultimo_consumo = models.DateField(null=True)
    conductas_sex_riesgo = models.TextField(max_length=300, null=True)
    intervenciones_previas = models.TextField(max_length=300, null=True)
    consumo_familiar = models.BooleanField(default=False)
    vinculo = models.TextField(max_length=300, null=True)

    tendencia_suicida = models.ForeignKey(
        SiNoNunca, on_delete=models.CASCADE, related_name='hpc_tendencia_suicida')
    presencia_planeacion = models.ForeignKey(
        SiNoNunca, on_delete=models.CASCADE, related_name='hpc_presencia_planeacion')
    disponibilidad_medios = models.ForeignKey(
        SiNoNunca, on_delete=models.CASCADE, related_name='hpc_disponibilidad_medios')
    intentos_previos = models.IntegerField(default=0)
    fecha_ultimo_intento = models.DateField(null=True)
    manejo_hospitalario = models.BooleanField(null=True)
   
    metodo = models.TextField(max_length=300, null=True)
    letalidad = models.TextField(max_length=300, null=True)
    signos = models.TextField(max_length=300, null=True)
    tratamiento_psiquiatrico = models.ForeignKey(
        SiNoNunca, null=True, on_delete=models.CASCADE, related_name='hpc_tratamiento_psiquiatrico')
    estatus_persona = models.ForeignKey(
        EstatusPersona, on_delete=models.DO_NOTHING, null=True)
    acontecimientos_estresantes = models.TextField(max_length=300, null=True)
    historial_familiar = models.BooleanField(default=False)
    factores_protectores = models.TextField(max_length=300, null=True)
    red_apoyo = models.TextField(max_length=300, null=True)

    victima = models.BooleanField(default=False)
    tipo_violencia = models.TextField(max_length=300, null=True)
    agresor = models.TextField(max_length=300, null=True)
    inst_reporte_legal = models.TextField(max_length=300, null=True)

    asistencia_cita = models.BooleanField(default=False)
    contacto = models.BooleanField(default=False)
    contacto_interrumpido = models.BooleanField(default=False)
    inicia_otro_programa = models.BooleanField(default=False)
    p_tamizaje = models.TextField(max_length=300, null=True)
    c_o_d = models.TextField(max_length=300, null=True)
    anotaciones_antecedentes_psiquiatricos = models.TextField(
        max_length=5000, null=True)
    anotaciones_consumoSPA = models.TextField(max_length=5000, null=True)
    anotaciones_comportamiento_suic = models.TextField(
        max_length=5000, null=True)
    anotaciones_antecedentes_violencia = models.TextField(
        max_length=5000, null=True)
    anotaciones_libres_profesional = models.TextField(
        max_length=5000, null=True)
    seguimiento1 = models.TextField(max_length=5000, null=True)
    seguimiento2 = models.TextField(max_length=5000, null=True)

# Rompimientos
class RHPCSituacionContacto(models.Model):
    id_asesoria = models.ForeignKey(HPC, on_delete=models.CASCADE)
    id_situacion = models.ForeignKey(
        HPCSituacionContacto, on_delete=models.CASCADE)


class RHPCTiposDemandas(models.Model):
    id_asesoria = models.ForeignKey(HPC, on_delete=models.CASCADE)
    id_tipo_demanda = models.ForeignKey(
        HPCTiposDemandas, on_delete=models.CASCADE)


class RHPCTiposRespuestas(models.Model):
    id_asesoria = models.ForeignKey(HPC, on_delete=models.CASCADE)
    id_respuesta = models.ForeignKey(
        HPCTiposRespuestas, on_delete=models.CASCADE)


class SPAActuales(models.Model):
    id_paciente = models.ForeignKey(InfoPacientes, on_delete=models.CASCADE)
    id_sustancia = models.ForeignKey(SPA, on_delete=models.CASCADE)


class RHPCConductasASeguir(models.Model):
    id_asesoria = models.ForeignKey(HPC, on_delete=models.CASCADE)
    id_conducta = models.ForeignKey(ConductasASeguir, on_delete=models.CASCADE)
