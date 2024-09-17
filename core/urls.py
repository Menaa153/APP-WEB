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
    path('inventario/', views.ver_inventario, name='ver_inventario'),
    path('inventario/ven', views.ver_inventario, name='ver_inventario_ven'),
    path('inventario/buscar/ven', views.buscar_producto, name='buscar_producto'),
    path('inventario/buscar/ven/talla', views.buscar_productotalla, name='buscar_productotalla'),
    path('inventario/buscar/ven/tipo', views.buscar_productotipo, name='buscar_productotipo'),
    path('inventario/buscar/', views.buscar_producto, name='buscar_producto'),
    path('inventario/editar/<int:pk>/', views.editar_eliminar_producto, name='editar_eliminar_producto'),
    path('registrar/venta/', views.registrar_venta, name='registrar_venta'),
    path('guardar_cuenta_cobro/', views.guardar_cuenta_cobro, name='guardar_cuenta_cobro'),
    path('gestionar_cliente/', views.ges_cliente, name='gestionar_cliente'),
    path('gestionar_cliente2/', views.gestionar_cliente, name='gestionar_cliente2'),
    path('eliminar_cliente/', views.eliminar_cliente, name='eliminar_cliente'),
    path('buscar_cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('capturar_datos_pedido2/<int:cuenta_cobro_id>/', views.capturar_datos_pedido2, name='capturar_datos_pedido2'),
    path('cuenta_cobro/<int:cuenta_cobro_id>/modificar_producto_seleccionado/', views.modificar_producto_seleccionado, name='modificar_producto_seleccionado'),
    path('cuenta_cobro/<int:cuenta_cobro_id>/modificar_producto_final/<str:codigo_producto>/', views.modificar_producto_final, name='modificar_producto_final'),
    path('cuenta_cobro/<int:cuenta_cobro_id>/eliminar_producto/<str:codigo_producto>/', views.eliminar_producto, name='eliminar_producto'),
    path('cuenta_cobro/<int:cuenta_cobro_id>/modificar_producto/<str:codigo_producto>/', views.modificar_producto_pagina, name='modificar_producto_pagina'),
    path('registrar-cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('cliente-exito/', views.cliente_exito, name='cliente_exito'), 
    path('autocomplete_codigo_prenda/', views.autocomplete_codigo_prenda, name='autocomplete_codigo_prenda'),
    path('autocomplete_tipo_prenda/', views.autocomplete_tipo_prenda, name='autocomplete_tipo_prenda'),
    path('autocomplete_talla/', views.autocomplete_talla, name='autocomplete_talla'),
    path('previsualizar/venta/', views.previsualizar_venta, name='previsualizar_venta'),
    path('obtener_datos_inventario/', views.obtener_datos_inventario, name='obtener_datos_inventario'),
    path('reporte_mensual/', views.reporte_mensual, name='reporte_mensual'),
    path('formulario_reporte/', views.reporte_mensual, name='formulario_reporte'),
    path('generar_reporte2/', views.generar_reporte2, name='generar_reporte2'),
    path('generar_reporteg/', views.generar_reporteg, name='generar_reporteg'),



]