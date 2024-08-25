from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, HistorialVentas, Venta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout

from django.contrib import messages
from .forms import UserRegisterForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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

def login(request):
    return render(request, 'login.html')


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
    return render(request, 'home.html')



def logout_view(request):
    logout(request)
    return redirect('login')





@login_required
def inventario_general_view(request):
    profile = request.user.profile
    if profile.cargo in ['Contador', 'Modista Jefe']:
        inventario = Producto.objects.all()
        return render(request, 'inventario_general.html', {'inventario': inventario})
    else:
        return redirect('acceso_denegado')

@login_required
def inventario_vendedora_view(request):
    profile = request.user.profile
    if profile.cargo == 'Vendedora':
        inventario = Producto.objects.filter(sede=profile.sede)
        return render(request, 'inventario_vendedora.html', {'inventario': inventario})
    else:
        return redirect('acceso_denegado')





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Cuenta creada para {user.username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



from django.shortcuts import render
from .models import Inventario  # Asegúrate de importar el modelo de Producto

def ver_inventarioo(request):
    inventario = Inventario.objects.all()  # Recupera todos los productos del inventario
    return render(request, 'ver_inventario.html', {'inventario': inventario})

def ver_inventario(request):
    user = request.user
    if user.last_name == 'Medellin':
        inventario = Inventario.objects.filter(sede='Medellin')
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
        producto = Inventario.objects.filter(codigo_prenda=codigo_prenda).first()
        return render(request, 'ver_inventario.html', {'producto': producto, 'inventario': Inventario.objects.all()})
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
