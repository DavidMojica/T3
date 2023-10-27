from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

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
###### MODELOS FORÁNEOS 1 a 1 ######
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
    
    
    
    

    