"""
URL configuration for T3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('sm_HPC/', views.sm_HPC, name="sm_HPC"),
    path('sm_llamadas/',views.sm_llamadas, name="sm_llamadas"),
    path('sm_historial_citas/', views.sm_historial_citas, name="sm_historial_citas"),
    path('sm_historial_llamadas/', views.sm_historial_llamadas, name="sm_historial_llamadas"),
    path('404_restricted_area/', views.restricted_area_404, name="404_restricted_area"),
    path('404_not_deployed/', views.not_deployed_404, name="404_not_deployed"),
    path('adminuser/', views.adminuser, name="adminuser"),
    path('adminregister/', views.adminregister, name="adminregister"),
    path('eventHandler', views.eventHandler, name="eventHandler"),
    path('detallesusurio/', views.detallesusuario, name="detallesusuario"), 
    path('edit_account/', views.edit_account, name="edit_account"),
    path('autodata/', views.autodata, name="autodata"),
    path('get_departamentos/', views.get_departamentos, name='get_departamentos'),
    path('get_municipios/', views.get_municipios, name='get_municipios'),
    path('pacientesView/',views.pacientesView, name='pacientesView'),
    path('detallespaciente/', views.detallespaciente, name="detallespaciente"),
    path('informes/', views.admininformes, name='informes'),
    path('generar_pdf/<int:año>/<int:mes>/', views.generar_pdf, name='generate_pdf'),
]
