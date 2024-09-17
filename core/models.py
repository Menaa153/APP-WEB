from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Inventario(models.Model):
    sede = models.CharField(max_length=100, null=True, blank=True)
    codigo_prenda = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50)
    talla = models.CharField(max_length=10)
    cantidad = models.IntegerField()
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    umbral_inventario = models.IntegerField(default=10)  # Umbral de notificación

    def __str__(self):
        return f"{self.tipo} {self.talla} ({self.codigo_prenda})"



class HistorialVentas(models.Model):
    documento_comprador = models.CharField(max_length=20, null=True, blank=True)
    codigo_prenda = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    sede = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Historial Venta {self.id} - {self.codigo_prenda}"




class Cliente(models.Model):
    institucion = models.CharField(max_length=255)
    nit = models.CharField(max_length=60)
    direccion = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255)
    fecha_registro = models.DateField(auto_now_add=True)



class HistorialCuentasdeCobro(models.Model):
    cliente = models.CharField(max_length=60)  # Relación con el cliente
    codigo_producto = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2)
    precio_total = models.DecimalField(max_digits=20, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cuenta {self.codigo_producto} para {self.cliente.nit} - {self.fecha}"
