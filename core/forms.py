from django import forms
from .models import Inventario, HistorialVentas, Venta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['codigo_prenda', 'tipo', 'talla', 'cantidad', 'precio_unidad']

class VentaForm(forms.ModelForm):
    class Meta:
        model = HistorialVentas
        fields = ['codigo_venta', 'documento_comprador']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['codigo_venta', 'codigo_prenda', 'cantidad', 'precio_unitario', 'precio_total']
