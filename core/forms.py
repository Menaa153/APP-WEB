from django import forms
from .models import Cliente


class CuentaCobroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['institucion', 'nit', 'direccion', 'municipio', 'departamento']