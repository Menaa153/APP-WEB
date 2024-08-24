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
#from .views import SignUpView
from django.contrib.auth import views as auth_views  # Asegúrate de importar auth_views 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login , name='login'),
    path('signup/', views.sigup , name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('signup/', SignUpView.as_view(), name='signup')
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    #path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    #path('inventario/', views., name='detalle_venta'),
    path('registrar_inventario/', views.registrar_inventario, name='registrar_inventario'),
    path('exito/', views.exito, name='exito')

]