from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Inventario, HistorialVentas, Venta, CuentaCobro, Producto
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string  
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
import csv
from num2words import num2words


def exito(request):
    return render(request, 'exito.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Autenticación por email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirige a la página principal después de iniciar sesión
            else:
                return render(request, 'login.html', {'error_message': 'Contraseña incorrecta.'})
        else:
            return render(request, 'login.html', {'error_message': 'Correo electrónico no encontrado.'})
        
    return render(request, 'login.html')




@login_required
def home_view(request):
    user = request.user
    if user.last_name == 'CONTADOR' or user.last_name == 'MODISTA JEFE':
        return render(request, 'home.html')
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
        
        
        # Crear un nuevo objeto Producto y guardarlo en la base de datos
        producto = Inventario(
            sede=sede,
            codigo_prenda=codigo_prenda,
            tipo=tipo,
            talla=talla,
            cantidad=cantidad,
            precio_unidad=precio_unidad
        )
        # Verificar si ya existe una prenda con el mismo código
        if Inventario.objects.filter(codigo_prenda=codigo_prenda).exists():
            # Si ya existe, mostrar un mensaje de error
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
        if user.last_name == 'BOGOTA':
            inventario = Inventario.objects.filter(sede='BOGOTA')
        elif user.last_name == 'CALI':
            inventario = Inventario.objects.filter(sede='CALI')
        elif user.last_name == 'MELGAR':
            inventario = Inventario.objects.filter(sede='MELGAR')
        elif user.last_name == 'VILLAVICENCIO':
            inventario = Inventario.objects.filter(sede='VILLAVICENCIO')
        elif user.last_name == 'PALANQUERO':
            inventario = Inventario.objects.filter(sede='PALANQUERO')
        elif user.last_name == 'TRECESQUINAS':
            inventario = Inventario.objects.filter(sede='TRECESQUINAS')
        else:
            inventario = Inventario.objects.all()  # Mostrar todo el inventario para otros cargos
    
    if user.last_name == 'CONTADOR' or user.last_name == 'MODISTA JEFE':
        return render(request, 'ver_inventario.html', {'inventario': inventario})
    else:
        return render(request, 'ver_inventario_ven.html', {'inventario': inventario})

def inventario2(request):
    sede = request.GET.get('sede', None)
    if sede:
        inventario = Inventario.objects.filter(sede=sede)
    else:
        inventario = Inventario.objects.all()
    
    return render(request, 'ver_inventario.html', {'inventario': inventario, 'sede_seleccionada': sede})



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
        
        # Filtrar inventario según la sede del usuario
        if user.last_name == 'BOGOTA':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='BOGOTA').first()
        elif user.last_name == 'CALI':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='CALI').first()
        elif user.last_name == 'MELGAR':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='MELGAR').first()
        elif user.last_name == 'VILLAVICENCIO':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='VILLAVICENCIO').first()
        elif user.last_name == 'PALANQUERO':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='PALANQUERO').first()
        elif user.last_name == 'TRECESQUINAS':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='TRECESQUINAS').first()
        else:
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda).first()
        
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




def editar_eliminar_producto(request, pk):
    producto = get_object_or_404(Inventario, pk=pk)
    
    if request.method == 'POST':
        if request.POST.get('accion') == 'actualizar':
            producto.sede = request.POST.get('sede')
            producto.tipo = request.POST.get('tipo')
            producto.talla = request.POST.get('talla')
            producto.cantidad = request.POST.get('cantidad')
            producto.precio_unidad = request.POST.get('precio_unidad')
            producto.save()
        elif request.POST.get('accion') == 'eliminar':
            producto.delete()
        return redirect('ver_inventario')
    
    return render(request, 'ver_inventario.html', {'producto': producto, 'inventario': Inventario.objects.all()})




def registrar_venta(request):
    if request.method == 'POST':
        documento_comprador = request.POST.get('documento')
        codigo_prenda = request.POST.get('codigo_prenda')
        cantidad = int(request.POST.get('cantidad'))
        precio_unitario = float(request.POST.get('precio_unitario'))
        precio_total = cantidad * precio_unitario
        
        try:
            # Obtener la prenda del inventario usando el código
            prenda = Inventario.objects.get(codigo_prenda=codigo_prenda)
            
            # Verificar si hay suficiente cantidad en inventario
            if prenda.cantidad < cantidad:
                return render(request, 'registrar_venta.html', {'error': 'Cantidad insuficiente en inventario'})
            
            # Crear la venta primero
            venta = Venta.objects.create(
                documento_comprador=documento_comprador,
                codigo_prenda=codigo_prenda,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                precio_total=precio_total,
                sede=request.user.last_name
            )
            
            # Actualizar la cantidad en inventario
            prenda.cantidad -= cantidad
            prenda.save()
            
            
            # Luego crear el registro en HistorialVentas, asegurando que se relacione con la venta
            HistorialVentas.objects.create(
                documento_comprador=documento_comprador,
                codigo_prenda=codigo_prenda,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                precio_total=precio_total,
                fecha=timezone.now(),
                sede=request.user.last_name
            )
            
            #Verificar que el numero de disónible no este por debajo del stock permitido
            verificar_inventario_bajo(prenda)
            
            return render(request, 'registrar_venta.html', {'success': True})
        
        except Inventario.DoesNotExist:
            return render(request, 'registrar_venta.html', {'error': 'Prenda no encontrada'})
        
    return render(request, 'registrar_venta.html')



def generar_recibo(request):
    if request.method == 'POST':
        documento_comprador = request.POST.get('documento')
        
        # Obtener los datos de la venta según el documento
        ventas = HistorialVentas.objects.filter(documento_comprador=documento_comprador)
        
        if not ventas:
            return render(request, 'generar_recibo.html', {'error': 'No se encontraron ventas para el documento proporcionado'})
        
        # Calcular el total
        total_general = sum(venta.precio_total for venta in ventas)
        
        # Generar el HTML para el PDF
        html_string = render_to_string('recibo_pdf.html', {
            'ventas': ventas,
            'documento_comprador': documento_comprador,
            'total_general': total_general
        })
        
        # Crear el PDF usando xhtml2pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=recibo.pdf'
        
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        
        return response
    
    return render(request, 'generar_recibo.html')



def verificar_inventario_bajo(inventario):
    if inventario.cantidad < inventario.umbral_inventario:
        enviar_notificacion(inventario)



def enviar_notificacion(inventario):
    subject = f"Alerta de Inventario Bajo: {inventario.tipo}"
    message = f"El producto {inventario.tipo} de la sede {inventario.sede} con código {inventario.codigo_prenda} tiene una cantidad baja de {inventario.cantidad} en el inventario."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['jdesneidermena15@gmail.com']
    send_mail(subject, message, email_from, recipient_list)



def importar_csv_a_bd(request):
    if request.method == "POST" and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        # Asegúrate de que el archivo es un CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("El archivo no es un CSV.")

        # Leer el archivo CSV
        file_data = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(file_data)

        for row in reader:
            Inventario.objects.create(
                sede=row['sede'],
                codigo_prenda=row['codigo_prenda'],
                tipo=row['tipo'],
                talla=row['talla'],
                cantidad=int(row['cantidad']),
                precio_unidad=float(row['precio_unidad']),
                umbral_inventario=int(row['umbral_inventario'])
            )

        return HttpResponse("Datos importados exitosamente.")

    return render(request, 'importar_csv.html')



def cuenta_cobro_form(request):
    # Obtener la lista de productos desde la sesión, o una lista vacía si no existe
    productos = request.session.get('productos', [])
    return render(request, 'cuenta_cobro_form.html', {'productos': productos})

def agregar_producto(request):
    if request.method == 'POST':
        # Si la lista de productos no existe en la sesión, la inicializamos
        if 'productos' not in request.session:
            request.session['productos'] = []

        codigo_prenda = request.POST.get('codigo_producto')
        nombre = request.POST.get('producto_nombre')
        cantidad = int(request.POST.get('cantidad'))
        precio = float(request.POST.get('precio'))
        total = cantidad * precio

        # Añadimos el nuevo producto a la lista en la sesión
        productos = request.session['productos']
        productos.append({
            'codigo_prenda':codigo_prenda,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'total': total
        })

        # Guardamos la lista de vuelta en la sesión
        request.session['productos'] = productos

        # Guardamos la sesión para asegurarnos de que los cambios persisten
        request.session.modified = True

        return redirect('cuenta_cobro_form')

    # Si no es un POST, volvemos a mostrar la página con los productos de la sesión
    return render(request, 'cuenta_cobro_form.html', {'productos': request.session.get('productos', [])})



def capturar_datos_cliente(request):
    if request.method == 'POST':
        # Guardar datos del cliente en la sesión
        request.session['institucion'] = request.POST['institucion']
        request.session['nit'] = request.POST['nit']
        request.session['direccion'] = request.POST['direccion']
        request.session['municipio'] = request.POST['municipio']
        request.session['departamento'] = request.POST['departamento']
        
        # Redirigir a la vista para capturar los datos del pedido
        return redirect('capturar_datos_pedido')

    return render(request, 'capturar_datos_cliente.html')



@csrf_exempt
def capturar_datos_pedido(request):
    if request.method == 'POST':
        try:
            cantidad = float(request.POST['cantidad'])
            valor_unitario = float(request.POST['valor_unitario'])
        except ValueError:
            return render(request, 'capturar_datos_pedido.html', {
                'error_message': 'Cantidad y Valor Unitario deben ser números válidos.'
            })

        valor_total = cantidad * valor_unitario

        producto = {
            'codigo_producto': request.POST['codigo_producto'],
            'descripcion': request.POST['descripcion'],
            'cantidad': cantidad,
            'valor_unitario': valor_unitario,
            'valor_total': valor_total
        }

        if 'productos' not in request.session:
            request.session['productos'] = []

        request.session['productos'].append(producto)
        request.session.modified = True

        return redirect('capturar_datos_pedido')

    cliente = {
        'institucion': request.session.get('institucion', ''),
        'nit': request.session.get('nit', ''),
        'direccion': request.session.get('direccion', ''),
        'municipio': request.session.get('municipio', ''),
        'departamento': request.session.get('departamento', ''),
    }
    productos = request.session.get('productos', [])

    # Calcular el total acumulado
    total_a_pagar = sum(producto['valor_total'] for producto in productos)
    
    return render(request, 'capturar_datos_pedido.html', {
        'cliente': cliente,
        'productos': productos,
        'total_a_pagar': total_a_pagar
    })



def confirmacion(request):
    return render(request, 'confirmacion.html')


def guardar_cuenta_cobro(request):
    if request.method == 'POST':
        cliente = {
            'institucion': request.session.get('institucion'),
            'nit': request.session.get('nit'),
            'direccion': request.session.get('direccion'),
            'municipio': request.session.get('municipio'),
            'departamento': request.session.get('departamento')
        }

        productos = request.session.get('productos', [])
        concepto = request.POST.get('concepto', '')  # Obtener el concepto del formulario

        # Crear y guardar los productos
        producto_objects = []
        for prod in productos:
            producto = Producto(
                codigo_producto=prod['codigo_producto'],
                descripcion=prod['descripcion'],
                cantidad=int(prod['cantidad']),
                valor_unitario=float(prod['valor_unitario'])
            )
            producto.save()
            producto_objects.append(producto)

        # Crear y guardar la cuenta de cobro
        cuenta_cobro = CuentaCobro(
            institucion=cliente['institucion'],
            nit=cliente['nit'],
            direccion=cliente['direccion'],
            municipio=cliente['municipio'],
            departamento=cliente['departamento']
        )
        cuenta_cobro.save()
        cuenta_cobro.productos.set(producto_objects)

        # Crear un contexto con los datos necesarios para el PDF
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

        # Crear el contexto para el template
        context = {
            'institucion': cliente['institucion'],
            'nit': cliente['nit'],
            'direccion': cliente['direccion'],
            'municipio': cliente['municipio'],
            'departamento': cliente['departamento'],
            'productos': productos_con_totales,
            'total': total_general,
            'fecha_creacion': cuenta_cobro.fecha_creacion.strftime('%Y-%m-%d'),
            'total_formateado': total_formateado,
            'concepto': concepto  # Añadir concepto al contexto
        }

        # Generar el PDF
        template_path = 'cuentadecobro.html'
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
