from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

# Create your models here.
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
    