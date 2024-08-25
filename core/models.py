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



class Venta(models.Model):
    documento_comprador = models.CharField(max_length=20, null=True, blank=True)
    codigo_prenda = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    sede = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.codigo_venta} - {self.codigo_prenda}"
