from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Inventario, HistorialVentas, Cliente, HistorialCuentasdeCobro
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .forms import CuentaCobroForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string  
from django.core.mail import send_mail
from django.conf import settings
#from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from num2words import num2words
from datetime import datetime
from django.http import JsonResponse










def exito(request):
    return render(request, 'exito.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        #autenticación por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  #redirige a la pagina principal después de iniciar sesion
            else:
                return render(request, 'login.html', {'error_message': 'Contraseña incorrecta.'})
        else:
            return render(request, 'login.html', {'error_message': 'Correo electrónico no encontrado.'})
        
    return render(request, 'login.html')




@login_required
def home_view(request):
    user = request.user
    if user.last_name == 'CONTADOR':
        return render(request, 'home.html')
    
    elif user.last_name =='MODISTA JEFE':
        return render(request, 'home_modista.html')

    else:
        return render(request, 'home_vendedoras.html')



def logout_view(request):
    logout(request)
    return redirect('login')


def registrar_inventario(request):
    if request.method == 'POST':
        
        sede = request.POST.get('sede')
        codigo_prenda = request.POST.get('codigo_prenda')
        tipo = request.POST.get('tipo')
        talla = request.POST.get('talla')
        cantidad = request.POST.get('cantidad')
        precio_unidad = request.POST.get('precio_unidad')
        
        
        #crear un nuevo objeto Producto y guardarlo en la base de datos
        producto = Inventario(
            sede=sede,
            codigo_prenda=codigo_prenda,
            tipo=tipo,
            talla=talla,
            cantidad=cantidad,
            precio_unidad=precio_unidad
        )
        #verificar si ya existe una prenda con el mismo ccdigo
        if Inventario.objects.filter(codigo_prenda=codigo_prenda).exists():
            #si ya existe mostrar un mensaje de error
            return render(request, 'registrar_inventario.html', {'error': '¡Prenda ya existe!'})
        producto.save()
        
        return render(request, 'registrar_inventario.html', {'success': True})
    
    return render(request, 'registrar_inventario.html')



def ver_inventario(request):
    user = request.user
    sede = request.GET.get('sede')  # Obtener el parámetro 'sede' de la solicitud GET
    
    if sede:
        inventario = Inventario.objects.filter(sede=sede)
    else:
        if user.last_name == 'MODISTA JEFE':
            inventario = Inventario.objects.all()  # Mostrar todo el inventario para otros cargos
        else:
            inventario = Inventario.objects.filter(sede=user.last_name)
    
    if user.last_name == 'CONTADOR' or user.last_name == 'MODISTA JEFE':
        return render(request, 'ver_inventario.html', {'inventario': inventario})
    else:
        return render(request, 'ver_inventario_ven.html', {'inventario': inventario})



def editar_inventario(request, pk):
    producto = get_object_or_404(Inventario, pk=pk)
    
    if request.method == 'POST':
        producto.cantidad = request.POST.get('cantidad')
        producto.precio_unidad = request.POST.get('precio_unidad')
        producto.save()
        return redirect('ver_inventario')
    
    return render(request, 'ver_inventario.html', {'inventario': Inventario.objects.all()})



def buscar_producto(request):
    if request.method == 'POST':
        codigo_prenda = request.POST.get('codigo_prenda')
        user = request.user
        
        if user.last_name == 'MODISTA JEFE':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda).first()
        else:
            # Filtrar inventario según la sede del usuario
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede=user.last_name).first()
        
        if producto:
            User = request.user
            if user.last_name == 'CONTADOR' or user.last_name == 'MODISTA JEFE':
                return render(request, 'ver_inventario.html', {'producto': producto, 'inventario': [producto]})
            else:
                return render(request, 'ver_inventario_ven.html', {'producto': producto, 'inventario': [producto]})
            
        else:
            messages.error(request, "Producto no encontrado en el inventario.")
            return redirect('ver_inventario')
        
    return redirect('ver_inventario')

def buscar_productotalla(request):
    if request.method == 'POST':
        talla = request.POST.get('talla')
        user = request.user
        
        if user:
            # Filtrar inventario según la sede del usuario
            productos = Inventario.objects.filter(talla=talla, sede=user.last_name)
        else:
            productos = Inventario.objects.filter(talla=talla)
        
        if productos.exists():
            # Dependiendo del tipo de usuario, renderiza la vista correspondiente
            if user.last_name == 'CONTADOR' or user.last_name == 'MODISTA JEFE':
                return render(request, 'ver_inventario.html', {'inventario': productos})
            else:
                return render(request, 'ver_inventario_ven.html', {'inventario': productos})
        else:
            messages.error(request, "Producto no encontrado en el inventario.")
            return redirect('ver_inventario')
        
    return redirect('ver_inventario')


def buscar_productotipo(request):
    if request.method == 'POST':
        tipo_prenda = request.POST.get('tipo_prenda')
        user = request.user
        
        if user:
            # Filtrar inventario según la sede del usuario
            productos = Inventario.objects.filter(tipo=tipo_prenda, sede=user.last_name)
        else:
            productos = Inventario.objects.filter(tipo=tipo_prenda)
        
        
        if productos.exists():
            # Dependiendo del tipo de usuario, renderiza la vista correspondiente
            if user.last_name == 'CONTADOR' or user.last_name == 'MODISTA JEFE':
                return render(request, 'ver_inventario.html', {'inventario': productos})
            else:
                return render(request, 'ver_inventario_ven.html', {'inventario': productos})
        else:
            messages.error(request, "Producto no encontrado en el inventario.")
            return redirect('ver_inventario')
        
    return redirect('ver_inventario')


def editar_eliminar_producto(request, pk):
    producto = get_object_or_404(Inventario, pk=pk)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'editar': 
            producto.sede = request.POST.get('sede')
            producto.tipo = request.POST.get('tipo')
            producto.talla = request.POST.get('talla')
            producto.cantidad = request.POST.get('cantidad')
            producto.precio_unidad = request.POST.get('precio')
            producto.save()
            messages.success(request, "Producto actualizado correctamente.")
        elif accion == 'eliminar':
            producto.delete()
            messages.success(request, "Producto eliminado correctamente.")
        return redirect('ver_inventario')

    return render(request, 'ver_inventario.html', {'producto': producto, 'inventario': Inventario.objects.all()})






# Vista para registrar la venta
def registrar_venta(request):
    if request.method == 'POST':
        documento = request.POST.get('documento')
        codigo_prenda = request.POST.get('codigo_prenda')
        cantidad = int(request.POST.get('cantidad'))

        try:
            # Verificamos si existe la prenda en el inventario
            prenda = Inventario.objects.get(codigo_prenda=codigo_prenda)
            
            # Verificamos si hay suficiente inventario
            if prenda.cantidad >= cantidad:
                # Calculamos el precio total
                precio_total = prenda.precio_unidad * cantidad
                # Obtener la fecha y hora actual
                fecha = datetime.now()  

                # Creamos el registro de la venta
                venta = HistorialVentas.objects.create(
                    documento_comprador=documento,
                    codigo_prenda=prenda.codigo_prenda,
                    cantidad=cantidad,
                    precio_unitario=prenda.precio_unidad,
                    precio_total=precio_total,
                    fecha=fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    sede=request.user.last_name
                )

                # Actualizamos el inventario
                prenda.cantidad -= cantidad
                prenda.save()
                
                #verificar que el numero de disonible no este por debajo del stock permitido
                verificar_inventario_bajo(prenda)
                # Mensaje de éxito
                messages.success(request, 'Venta registrada exitosamente')

                return redirect('registrar_venta')  # Redirigimos a la misma página para registrar otra venta

            else:
                # Si no hay suficiente inventario, mostramos un mensaje de error
                messages.error(request, 'No hay suficiente cantidad en inventario')
                """
                #PARAMETROS PARA ENVIAR CORREO A LA MODISTA
                subject = f"CANTIDAD DE INVENTARIO INSUFICIENTE EN: {prenda.sede}"
                message = f"En la sede {prenda.sede} se ha intentado vender {cantidad} prendas del producto ({prenda.codigo_prenda} - {prenda.tipo}, talla {prenda.talla}), se debe enviar a este punto de venta la candtidad de {(cantidad-prenda.cantidad)+10} prendas."
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['jdesneidermena15@gmail.com']
                send_mail(subject, message, email_from, recipient_list)
                """

        except Inventario.DoesNotExist:
            # Si la prenda no existe, mostramos un mensaje de error
            messages.error(request, 'La prenda no se encuentra en inventario')

    return render(request, 'registrar_venta.html')




# Vista para el autocompletado del código de prenda

def autocomplete_codigo_prenda(request):
    if 'term' in request.GET:
        qs = Inventario.objects.filter(codigo_prenda__icontains=request.GET.get('term'))
        codes = list(qs.values_list('codigo_prenda', flat=True))
        return JsonResponse(codes, safe=False)


# Vista para previsualizar la venta
def previsualizar_venta(request):
    if 'codigo_prenda' in request.GET and 'cantidad' in request.GET:
        codigo_prenda = request.GET.get('codigo_prenda')
        cantidad = int(request.GET.get('cantidad'))
        
        try:
            prenda = Inventario.objects.get(codigo_prenda=codigo_prenda)
            
            if prenda.cantidad < cantidad:
                return JsonResponse({'error': 'Cantidad insuficiente en inventario'})
            
            precio_unitario = prenda.precio_unidad
            total_pagar = precio_unitario * cantidad
            
            return JsonResponse({
                'codigo_prenda': prenda.codigo_prenda,
                'precio_unitario': precio_unitario,
                'cantidad_inventario': prenda.cantidad,
                'total_pagar': total_pagar
            })
        
        except Inventario.DoesNotExist:
            return JsonResponse({'error': 'Prenda no encontrada'})

    return JsonResponse({'error': 'Datos incompletos'})



def obtener_datos_inventario(request):
    codigo_prenda = request.GET.get('codigo_prenda', None)
    
    if codigo_prenda:
        try:
            prenda = Inventario.objects.get(codigo_prenda=codigo_prenda)
            data = {
                'precio_unitario': prenda.precio_unidad,
                'cantidad_inventario': prenda.cantidad
            }
            return JsonResponse(data)
        except Inventario.DoesNotExist:
            return JsonResponse({'error': 'Prenda no encontrada'}, status=404)
    else:
        return JsonResponse({'error': 'Código de prenda no proporcionado'}, status=400)




def verificar_inventario_bajo(inventario):
    if inventario.cantidad < inventario.umbral_inventario:
        enviar_notificacion(inventario)


def enviar_notificacion(inventario):
    #PARAMETROS PARA ENVIAR CORREO A LA MODISTA
    subject = f"Alerta de Inventario CRITICO: {inventario.tipo}"
    message = f"El producto {inventario.tipo} de la sede {inventario.sede} con código {inventario.codigo_prenda} tiene una cantidad critica de {inventario.cantidad} en el inventario."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['jdesneidermena15@gmail.com']
    send_mail(subject, message, email_from, recipient_list)




def guardar_cuenta_cobro(request):
    if request.method == 'POST':
        # Datos del cliente desde la sesión
        cliente = {
            'institucion': request.session.get('institucion'),
            'nit': request.session.get('nit'),
            'direccion': request.session.get('direccion'),
            'municipio': request.session.get('municipio'),
            'departamento': request.session.get('departamento')
        }
        
        # Lista de productos desde la sesión
        productos = request.session.get('productos', [])
        concepto = request.POST.get('concepto', '')  # Concepto que se introdujo en el formulario
        
        # Guardar los productos en la tabla de HistorialCuentasdeCobro
        producto_objects = []
        for prod in productos:
            cantidad = int(prod['cantidad'])
            valor_unitario = float(prod['valor_unitario'])
            precio_total = cantidad * valor_unitario  # Calcular precio total

            producto = HistorialCuentasdeCobro(
                codigo_producto=prod['codigo_producto'],
                descripcion=prod['descripcion'],
                cantidad=cantidad,
                valor_unitario=valor_unitario,
                precio_total=precio_total,
                fecha=datetime.now(),
                cliente=cliente['nit']  # Guardar el NIT del cliente
            )
            producto.save()
            producto_objects.append(producto)

        # Calcular los totales para el PDF
        productos_con_totales = []
        total_general = 0
        
        for p in productos:
            cantidad = int(p['cantidad'])
            valor_unitario = float(p['valor_unitario'])
            valor_total = cantidad * valor_unitario
            total_general += valor_total
            
            productos_con_totales.append({
                'codigo_producto': p['codigo_producto'],
                'descripcion': p['descripcion'],
                'cantidad': cantidad,
                'valor_unitario': valor_unitario,
                'valor_total': valor_total
            })
        
        # Convertir el total a letras
        total_letras = num2words(total_general, lang='es').capitalize()
        total_formateado = f"{total_letras} (${total_general:,.2f})"
        
        # Crear el contexto para el PDF
        context = {
            'institucion': cliente['institucion'],
            'nit': cliente['nit'],
            'direccion': cliente['direccion'],
            'municipio': cliente['municipio'],
            'departamento': cliente['departamento'],
            'productos': productos_con_totales,
            'total': total_general,
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d'),
            'total_formateado': total_formateado,
            'concepto': concepto  # Añadir concepto al contexto
        }
        
        # Generar el PDF
        template_path = 'cuentadecobro.html'  # Ruta al template HTML
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cuenta_cobro.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF')
        
        # Limpiar la sesión de productos
        request.session.pop('productos', None)
        
        return response
    return redirect('capturar_datos_cliente')



def ges_cliente(request):
    return render(request, 'gestionar_con.html')


def gestionar_cliente(request):
    clientes = []  # Inicializa la variable clientes
    form = None
    error = None
    
    if request.method == 'POST':
        nit = request.POST.get('nit')
        action = request.POST.get('action')  # edit or delete
        
        if nit:
            clientes = Cliente.objects.filter(nit=nit)
            
            if action == 'edit':
                if clientes.exists():
                    for cliente in clientes:
                        form = CuentaCobroForm(request.POST, instance=cliente)
                        if form.is_valid():
                            form.save()
                    messages.success(request, "Clientes actualizados exitosamente.")
                    return redirect('gestionar_cliente')
                else:
                    messages.error(request, "No se encontraron clientes para actualizar.")
        else:
            messages.error(request, "NIT no encontrado")
            return render(request, 'gestionar_cliente.html')
            
            
            
    if request.method == 'GET':
        nit = request.GET.get('nit')
        if nit:
            clientes = Cliente.objects.filter(nit=nit)
            if clientes.exists():
                #mostrar solo el primer registro para el formulario
                form = CuentaCobroForm(instance=clientes.first())
                
    return render(request, 'gestionar_cliente.html', {
        'clientes': clientes,
        'form': form,
        'error': error,
    })


def eliminar_cliente(request):
    clientes = []  # Inicializa la variable clientes
    form = None
    error = None
    
    if request.method == 'POST':
        nit = request.POST.get('nit')
        action = request.POST.get('action')  # edit or delete
        
        if nit:
            clientes = Cliente.objects.filter(nit=nit)
            
            if action == 'delete':
                if clientes.exists():
                    clientes.delete()
                    messages.success(request, "Clientes eliminados exitosamente.")
                    return redirect('eliminar_cliente')
                else:
                    messages.error(request, "No se encontraron clientes para eliminar.")
                    
        else:
            messages.error(request, "NIT no encontrado")
            return render(request, 'eliminar_cliente.html')
            
            
            
    if request.method == 'GET':
        nit = request.GET.get('nit')
        if nit:
            clientes = Cliente.objects.filter(nit=nit)
            if clientes.exists():
                #mostrar solo el primer registro para el formulario
                form = CuentaCobroForm(instance=clientes.first())
                
    return render(request, 'eliminar_cliente.html', {
        'clientes': clientes,
        'form': form,
        'error': error,
    })



def buscar_cliente(request):
    if request.method == 'POST':
        nit = request.POST.get('nit', None)
        if nit:
            cuenta_cobros = Cliente.objects.filter(nit=nit)
            if cuenta_cobros.exists():
                cuenta_cobro = cuenta_cobros.first()
                
                # Guardar los datos del cliente en la sesión
                request.session['institucion'] = cuenta_cobro.institucion
                request.session['nit'] = cuenta_cobro.nit
                request.session['direccion'] = cuenta_cobro.direccion
                request.session['municipio'] = cuenta_cobro.municipio
                request.session['departamento'] = cuenta_cobro.departamento
                
                return redirect('capturar_datos_pedido2', cuenta_cobro_id=cuenta_cobro.id)
            else:
                messages.error(request, "NIT no encontrado")
                return render(request, 'buscar_cliente.html')
        else:
            messages.error(request, "Por favor, ingresa un NIT.")
            return render(request, 'buscar_cliente.html')
    return render(request, 'buscar_cliente.html')



def datos_pedido(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    productos = request.session.get('productos', [])
    
    total_a_pagar = sum([p['valor_total'] for p in productos])
    context = {
        'cliente': cliente,
        'productos': productos,
        'total_a_pagar': total_a_pagar,
    }
    return render(request, 'nuevo.html', context)



def capturar_datos_pedido2(request, cuenta_cobro_id):
    cuenta_cobro = get_object_or_404(Cliente, id=cuenta_cobro_id)
    
    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo_producto')
        cantidad = request.POST.get('cantidad')
        
        try:
            # Consultar el producto en la tabla Inventario
            inventario_producto = Inventario.objects.get(codigo_prenda=codigo_producto)
            cantidad = int(cantidad)
            valor_unitario = inventario_producto.precio_unidad
            valor_total = cantidad * valor_unitario
            
            # Almacenar el producto en la sesión
            producto = {
                'codigo_producto': codigo_producto,
                'descripcion': f'{inventario_producto.tipo} TALLA {inventario_producto.talla}',  # Puedes obtener la descripción del inventario
                'cantidad': cantidad,
                'valor_unitario': valor_unitario,
                'valor_total': valor_total
            }
            
            if 'productos' not in request.session:
                request.session['productos'] = []
                
            request.session['productos'].append(producto)
            request.session.modified = True
            
            return redirect('capturar_datos_pedido2', cuenta_cobro_id=cuenta_cobro_id)
        
        except Inventario.DoesNotExist:
            error_message = 'Producto no encontrado en el inventario.'
            
        except ValueError:
            error_message = 'La cantidad debe ser un número válido.'
    else:
        error_message = None
        
    # Obtener los productos almacenados en la sesión para que sigan mostrándose
    productos = request.session.get('productos', [])
    total_a_pagar = sum([p['valor_total'] for p in productos])
    
    context = {
        'cuenta_cobro': cuenta_cobro,
        'productos': productos,
        'total_a_pagar': total_a_pagar,
        'error_message': error_message,  # Pasar el mensaje de error al contexto
    }
    return render(request, 'nuevo.html', context)




def modificar_producto_final(request, cuenta_cobro_id, codigo_producto):
    cuenta_cobro = get_object_or_404(Cliente, id=cuenta_cobro_id)
    if request.method == 'POST':
        nueva_cantidad = request.POST.get('cantidad')
        
        productos = request.session.get('productos', [])
        print("Productos antes de modificar:", productos)  # Para verificar los productos antes del cambio
        for producto in productos:
            if producto['codigo_producto'] == codigo_producto:
                producto['cantidad'] = int(nueva_cantidad)
                producto['valor_total'] = int(nueva_cantidad) * producto['valor_unitario']
                print("Producto modificado:", producto)  # Verificar el cambio realizado
                
        request.session['productos'] = productos
        print("Productos después de modificar:", request.session['productos'])  # Verificar después de guardar en sesión
        return redirect('capturar_datos_pedido2', cuenta_cobro_id=cuenta_cobro_id)


def eliminar_producto(request, cuenta_cobro_id, codigo_producto):
    cuenta_cobro = get_object_or_404(Cliente, id=cuenta_cobro_id)
    if request.method == 'POST':
        productos = request.session.get('productos', [])
        productos = [p for p in productos if p['codigo_producto'] != codigo_producto]
        
        request.session['productos'] = productos
        return redirect('capturar_datos_pedido2', cuenta_cobro_id=cuenta_cobro_id)


def modificar_producto_seleccionado(request, cuenta_cobro_id):
    cuenta_cobro = get_object_or_404(Cliente, id=cuenta_cobro_id)
    if request.method == 'POST':
        # Captura el valor del producto seleccionado
        codigo_producto = request.POST.get('producto_seleccionado')
        
        if codigo_producto:
            # Si el producto está seleccionado, redirige a la página de modificar
            return redirect('modificar_producto_pagina', cuenta_cobro_id=cuenta_cobro_id, codigo_producto=codigo_producto)
        else:
            # Si no se seleccionó ningún producto, muestra un mensaje de error
            messages.error(request, "No seleccionaste ningún producto.")
            return redirect('capturar_datos_pedido2', cuenta_cobro_id=cuenta_cobro_id)


def modificar_producto_pagina(request, cuenta_cobro_id, codigo_producto):
    cuenta_cobro = get_object_or_404(Cliente, id=cuenta_cobro_id)
    
    productos = request.session.get('productos', [])
    producto = next((p for p in productos if p['codigo_producto'] == codigo_producto), None)
    
    if producto:
        print(f"Producto encontrado: {producto}")
        context = {
            'cuenta_cobro': cuenta_cobro,
            'producto': producto
        }
        return render(request, 'modificar_producto_pagina.html', context)
    else:
        print(f"Producto con código {codigo_producto} no encontrado.")
        messages.error(request, "Producto no encontrado.")
        return redirect('capturar_datos_pedido2', cuenta_cobro_id=cuenta_cobro_id)


def registrar_cliente(request):
    if request.method == 'POST':
        institucion = request.POST.get('institucion')
        nit = request.POST.get('nit')
        direccion = request.POST.get('direccion')
        municipio = request.POST.get('municipio')
        departamento = request.POST.get('departamento')
        
        # Crear el objeto cliente
        cliente = Cliente(
            institucion=institucion,
            nit=nit,
            direccion=direccion,
            municipio=municipio,
            departamento=departamento
        )
        
        # Guardar en la base de datos
        cliente.save()
        
        # Redirigir después de guardar
        messages.success(request, "Cliente registrado exitosamente!!.")
        return redirect('registrar_cliente')
    
    return render(request, 'registrar_cliente.html')

def cliente_exito(request):
    return HttpResponse("Cliente registrado con éxito.")


def autocomplete_codigo_prenda(request):
    if 'term' in request.GET:
        qs = Inventario.objects.filter(codigo_prenda__icontains=request.GET.get('term'))
        codes = list(qs.values_list('codigo_prenda', flat=True))
        return JsonResponse(codes, safe=False)


def autocomplete_tipo_prenda(request):
    if 'term' in request.GET:
        qs = Inventario.objects.filter(tipo__icontains=request.GET.get('term'))
        types = list(qs.values_list('tipo', flat=True))
        return JsonResponse(types, safe=False)


def autocomplete_talla(request):
    if 'term' in request.GET:
        qs = Inventario.objects.filter(talla__icontains(request.GET.get('term')))
        sizes = list(qs.values_list('talla', flat=True))
        return JsonResponse(sizes, safe=False)





def reporte_mensual(request):
    if request.method == 'POST':
        # Obtenemos la fecha del formulario
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Convertimos las fechas a formato datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
        # Obtenemos la sede de la vendedora que está logueada
        sede_vendedora = request.user.last_name
        
        # Filtramos las ventas de esa sede dentro del rango de fechas
        ventas = HistorialVentas.objects.filter(
            sede=sede_vendedora,
            fecha__range=[fecha_inicio, fecha_fin]
        )
        
        # Pasamos las ventas al template de reporte
        return render(request, 'reporte_mensual.html', {'ventas': ventas})
    
    # Si no se envía nada, mostrar el formulario de fechas
    return render(request, 'formulario_reporte.html')




def generar_reporte2(request):
    if request.method == 'POST':
        # Obtenemos el tipo de reporte
        tipo_reporte = request.POST.get('tipo_reporte')
        sede = request.POST.get('sede')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Convertimos las fechas
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
        # Filtrar las ventas según el tipo de reporte
        if tipo_reporte == 'general':
            # Reporte general de todas las sedes
            ventas = HistorialVentas.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        else:
            # Reporte de una sede específica
            ventas = HistorialVentas.objects.filter(sede=sede, fecha__range=[fecha_inicio, fecha_fin])
            
        # Renderizamos el reporte con las ventas filtradas
        return render(request, 'reporte_ventas.html', {'ventas': ventas})
    
    return render(request, 'formulario_reporte.html')


def generar_reporteg(request):
    return render(request, 'generar_reporteg.html')