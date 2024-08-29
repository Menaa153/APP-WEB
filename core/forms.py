from django import forms
from .models import CuentaCobro


class CuentaCobroForm(forms.ModelForm):
    class Meta:
        model = CuentaCobro
        fields = ['institucion', 'nit', 'direccion', 'municipio', 'departamento']