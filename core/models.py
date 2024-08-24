from django.db import models

# Create your models here.

class Inventario(models.Model):
    codigo_prenda = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50)
    talla = models.CharField(max_length=10)
    cantidad = models.IntegerField()
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo} {self.talla} ({self.codigo_prenda})"


class HistorialVentas(models.Model):
    codigo_venta = models.CharField(max_length=100, unique=True)
    codigo_prenda = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    documento_comprador = models.CharField(max_length=20)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.codigo_venta} - {self.documento_comprador}"


class Venta(models.Model):
    codigo_venta = models.ForeignKey(HistorialVentas, on_delete=models.CASCADE)
    codigo_prenda = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.codigo_venta} - {self.codigo_prenda}"

