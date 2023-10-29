from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Otros campos personalizados
    list_display = ('username', 'email', 'tipo_usuario')

admin.site.register(CustomUser, CustomUserAdmin)

def d():
    pass