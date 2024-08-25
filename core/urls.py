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
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view , name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
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
    path('exito/', views.exito, name='exito'),
    path('register/', views.register, name='register'),
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    path('inventario/buscar/', views.buscar_producto, name='buscar_producto'),
    path('inventario/editar/<int:pk>/', views.editar_eliminar_producto, name='editar_eliminar_producto'),

    
    #path('', views.home_view, name='home')

]