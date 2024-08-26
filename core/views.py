from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, HistorialVentas, Venta

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
from django.template.loader import render_to_string  # Asegúrate de tener esta línea
from django.core.mail import send_mail
from django.conf import settings


#def home(request):
#    return HttpResponse("Hello, World!")

"""
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'
"""
def sigup(request):
    return render(request, 'signup.html')

#def login(request):
#   return render(request, 'login.html')


def exito(request):
    return render(request, 'exito.html')


# Vistas para el manejo de productos
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def lista_productos(request):
    productos = Inventario.objects.all()
    return render(request, 'registrar_venta.html', {'productos': productos})

# Vistas para el manejo de ventas
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save()
            return redirect('detalle_venta', venta_id=venta.id)
    else:
        form = VentaForm()
    return render(request, 'crear_venta.html', {'form': form})

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVentaForm.objects.filter(venta=venta)
    return render(request, 'detalle_venta.html', {'venta': venta, 'detalles': detalles})

# core/views.py



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

        # Redirigir a una página de éxito o al mismo formulario
        #return redirect()  # Cambia 'success_url' por la URL que prefieras
        return render(request, 'registrar_inventario.html', {'success': True})

    return render(request, 'registrar_inventario.html')

"""
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user) # Aquí usamos auth_login en lugar de login
            return redirect('home')# Redirigir a la página de sede correspondinte
        
        else:
            return render(request, 'login.html', {'error_message': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'login.html')
"""



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
    if user.last_name == 'Contador' or user.last_name == 'Modista Jefe':
        return render(request, 'home.html')
    else:
        return render(request, 'home_vendedoras.html')



def logout_view(request):
    logout(request)
    return redirect('login')





from django.shortcuts import render
from .models import Inventario  # Asegúrate de importar el modelo de Producto

"""
def ver_inventarioo(request):
    inventario = Inventario.objects.all()  # Recupera todos los productos del inventario
    return render(request, 'ver_inventario.html', {'inventario': inventario})
"""


def ver_inventario(request):
    user = request.user
    if user.last_name == 'Medellin':
        inventario = Inventario.objects.filter(sede='Medellin')        
    elif user.last_name == 'Cali':
        inventario = Inventario.objects.filter(sede='Cali')
    elif user.last_name == 'Cartagena':
        inventario = Inventario.objects.filter(sede='Cartagena')
    elif user.last_name == 'Bogota':
        inventario = Inventario.objects.filter(sede='Bogota')
    else:
        inventario = Inventario.objects.all()  # Mostrar todo el inventario para otros cargos
    return render(request, 'ver_inventario.html', {'inventario': inventario})




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
        if user.last_name == 'Medellin':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='Medellin').first()
        elif user.last_name == 'Cali':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='Cali').first()
        elif user.last_name == 'Cartagena':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='Cartagena').first()
        elif user.last_name == 'Bogota':
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda, sede='Bogota').first()
        else:
            producto = Inventario.objects.filter(codigo_prenda=codigo_prenda).first()

        if producto:
            return render(request, 'ver_inventario.html', {'producto': producto, 'inventario': [producto]})
        else:
            messages.error(request, "Producto no encontrado en el inventario de tu sede.")
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
            #verificar_inventario_bajo(prenda)

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

