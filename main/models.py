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
            raise ValueError('Los superusuarios deben tener is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
#Tabla foránea
class TipoUsuario(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description.capitalize()
    
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.DO_NOTHING, default=3)
    objects = CustomUserManager()
    
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
    
class Pip(models.Model): #POBLACION IDENTIFICADA POR PARTICULARIDADES
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
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    pertenece_pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.description.capitalize()

class Municipio(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    pertenece_departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING)
    guardado_por = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, default=models.SET_NULL)
    
    def __str__(self):
        return self.description.capitalize()
    
class DiaNombre(models.Model):
    id = models.AutoField(primary_key=True)   
    description = models.CharField(max_length=15) 


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
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.DO_NOTHING)
    nombre = models.TextField(max_length=200)
    email = models.EmailField(max_length=254)
    fecha_nacimiento = models.DateField()
    escolaridad = models.ForeignKey(Escolaridad, on_delete=models.DO_NOTHING)
    numero_hijos = models.IntegerField(null=False)
    sexo = models.ForeignKey(Sexo, on_delete=models.DO_NOTHING)
    direccion = models.TextField(max_length=150)
    barrio = models.CharField(max_length=100)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.DO_NOTHING)
    telefono = models.CharField(null=True)
    celular = models.CharField(null=True)
    lectoescritura_indicador = models.ForeignKey(Lecto1, on_delete=models.DO_NOTHING)
    lectoescritura_nivel = models.ForeignKey(Lecto2, on_delete=models.DO_NOTHING)
    razonamiento_analitico = models.ForeignKey(Razonamiento, on_delete=models.DO_NOTHING)
    etnia = models.ForeignKey(Etnia, on_delete=models.DO_NOTHING)
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.DO_NOTHING)
    regimen_seguridad = models.ForeignKey(RegimenSeguridad, on_delete=models.DO_NOTHING)
    sisben = models.BooleanField(null=False)
    nombre_eps = models.CharField(max_length=50)
    cant_asesorias_psicologicas = models.IntegerField(default=0)
    cant_atenciones_urgencias = models.IntegerField(default=0)

#Rompimientos
class PacienteCalculo(models.Model):
    documento_usuario = models.ForeignKey(InfoPacientes, on_delete=models.DO_NOTHING)
    id_calculo = models.ForeignKey(Calculo, on_delete=models.DO_NOTHING)
    
class PacientePip(models.Model):
    documento_usuario = models.ForeignKey(InfoPacientes, on_delete=models.DO_NOTHING)
    id_pip = models.ForeignKey(Pip, on_delete=models.DO_NOTHING)
    

"""
##### MODELO DE INFORMACIÓN PARA TRABAJADORES #####
En este modelo se guarda la información de los trabajadores, es similar al de los pacientes
sólo que con algunos campos menos que se consideraron innecesarios.
"""
class InfoMiembros(models.Model):
    documento = models.CharField(primary_key=True, max_length=20, null=False)
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.DO_NOTHING)
    id_usuario = models.ForeignKey(TipoUsuario, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=255, null = True)
    numero_hijos = models.IntegerField(null=False, default=0)
    sexo = models.ForeignKey(Sexo, on_delete=models.DO_NOTHING)
    direccion = models.CharField(max_length=100, null = False)
    barrio = models.CharField(max_length=100, null = False)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.DO_NOTHING)
    telefono = models.CharField(null=True)
    celular = models.CharField(null=True)
    etnia = models.ForeignKey(Etnia, on_delete=models.DO_NOTHING)
    regimen_seguridad = models.ForeignKey(RegimenSeguridad, on_delete=models.DO_NOTHING)
    sisben = models.BooleanField(null=False)
    nombre_eps = models.CharField(max_length=50)
    contador_llamadas_psicologicas = models.IntegerField(null=False, default=0)
    contador_asesorias_psicologicas = models.IntegerField(null=False, default=0)
    
"""
##### MODELO DE INFORMACIÓN DE LLAMADAS #####
Aquí se guarda la información proveniente de las llamadas psicologicas.
"""


class PsiLlamadas(models.Model):
    id = models.AutoField(primary_key=True)
    documento = models.CharField(max_length=30, default=models.SET_NULL)
    nombre_paciente = models.CharField(null=True, max_length=100)
    id_psicologo = models.ForeignKey(InfoMiembros, on_delete=models.DO_NOTHING)
    
    fecha_llamada = models.DateField(default=timezone.now)
    dia_semana = models.ForeignKey(DiaNombre, on_delete=models.DO_NOTHING)
    hora = models.TimeField(auto_now_add=True)
    
    sexo = models.ForeignKey(Sexo, on_delete=models.DO_NOTHING)
    edad = models.IntegerField(null=True, default=models.SET_NULL)
    direccion = models.CharField(null=True, max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING)
    celular = models.CharField(null=True, max_length=30) 
    poblacion_vulnerable = models.CharField(null=True, max_length=100) 
    motivo_llamada = models.TextField(null=True, max_length=5000) 
    conducta_a_seguir = models.TextField(null=True, max_length=5000) 
    observaciones = models.TextField(null=True, max_length=5000)
    seguimiento24 = models.TextField(null=True, max_length=5000)
    seguimiento48 = models.TextField(null=True, max_length=5000)
    seguimiento72 = models.TextField(null=True, max_length=5000)

    def save(self, *args, **kwargs):
        # Obtener el número del día actual (1 para lunes, 2 para martes, etc.)
        dia_actual = datetime.datetime.now().isoweekday()
        self.dia_semana = dia_actual
        super(PsiLlamadas, self).save(*args, **kwargs)