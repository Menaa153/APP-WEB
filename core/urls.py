"""
URL configuration for confecciones project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('registrar_inventario/', views.registrar_inventario, name='registrar_inventario'),
    #path('exito/', views.exito, name='exito'),
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    path('inventario/buscar/', views.buscar_producto, name='buscar_producto'),
    path('inventario/editar/<int:pk>/', views.editar_eliminar_producto, name='editar_eliminar_producto'),
    path('registrar/venta/', views.registrar_venta, name='registrar_venta'),
    path('recibo/<str:documento>/', views.generar_recibo, name='generar_recibo'),
    path('generar/recibo/', views.generar_recibo, name='generar_recibo'),
]