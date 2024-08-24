from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, HistorialVentas, Venta
from .forms import ProductoForm, VentaForm, DetalleVentaForm
from django.shortcuts import render, redirect




def home(request):
    return HttpResponse("Hello, World!")

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
        codigo_prenda = request.POST.get('codigo_prenda')
        tipo = request.POST.get('tipo')
        talla = request.POST.get('talla')
        cantidad = request.POST.get('cantidad')
        precio_unidad = request.POST.get('precio_unidad')

        # Crear un nuevo objeto Producto y guardarlo en la base de datos
        producto = Inventario(
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


