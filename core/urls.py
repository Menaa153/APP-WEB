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
    #path('inventario/2', views.ver_inventario, name='inventario2'),
    path('inventario/ven', views.ver_inventario, name='ver_inventario_ven'),
    path('inventario/buscar/ven', views.buscar_producto, name='buscar_producto'),
    path('inventario/buscar/', views.buscar_producto, name='buscar_producto'),
    path('inventario/editar/<int:pk>/', views.editar_eliminar_producto, name='editar_eliminar_producto'),
    path('registrar/venta/', views.registrar_venta, name='registrar_venta'),
    path('recibo/<str:documento>/', views.generar_recibo, name='generar_recibo'),
    path('generar/recibo/', views.generar_recibo, name='generar_recibo'),
    #path('importar-csv/', views.importar_csv_a_bd, name='importar_csv'),
    #path('cuentacobro/', views.guardar_cuenta_cobro, name='guardar_cuenta_cobro'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('cobroform/', views.cuenta_cobro_form, name='cuenta_cobro_form'), 
    path('capturar_datos_cliente/', views.capturar_datos_cliente, name='capturar_datos_cliente'),
    path('capturar_datos_pedido/', views.capturar_datos_pedido, name='capturar_datos_pedido'),
    path('guardar_cuenta_cobro/', views.guardar_cuenta_cobro, name='guardar_cuenta_cobro'),
    path('gestionar_cliente/', views.gestionar_cliente, name='gestionar_cliente'),
    #path('gestionar_cliente2/', views.gestionar_cliente2, name='gestionar_cliente2'),
    #path('nuevo/', views.capturar_datos_pedido2, name='nuevo'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('gestionar_cliente2/', views.gestionar_cliente2, name='gestionar_cliente2'),
    #path('nuevo/', views.nuevoht, name='nuevo'),
    #path('capturar_datos_pedido/<int:cliente_id>/', views.capturar_datos_pedido2, name='capturar_datos_pedido'),
    #path('nuevo/', views.capturar_datos_pedido2, name='capturar_datos_pedido'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('capturar_datos_pedido2/<int:cuenta_cobro_id>/', views.capturar_datos_pedido2, name='capturar_datos_pedido2'),
]