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
    path('sm_HPC/', views.sm_HPC, name="sm_asesorias"),
    path('sm_llamadas/',views.sm_llamadas, name="sm_llamadas"),
    path('sm_historial/', views.sm_historial, name="sm_historial"),
    path('404_restricted_area/', views.restricted_area_404, name="404_restricted_area"),
    path('404_not_deployed/', views.not_deployed_404, name="404_not_deployed"),
    path('admon/', views.admon, name="admon"),
    path('edit_account/<int:user_id>/<int:user_type>/', views.edit_account, name="edit_account"),
    path('autodata/<int:user_id>/', views.autodata, name="autodata"),
    path('get_departamentos/', views.get_departamentos, name='get_departamentos'),
    path('get_municipios/', views.get_municipios, name='get_municipios'),
]
