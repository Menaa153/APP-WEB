# Generated by Django 5.1 on 2024-08-25 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_historialventas_codigo_venta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialventas',
            name='codigo_prenda',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='venta',
            name='codigo_prenda',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
