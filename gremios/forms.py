from django import forms
from .models import Certificacion


class CertificacionForm(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = ['antecedentes', 'certificado_vigencia', 'patente_comercial', 'poliza_seguro']
        labels = {
            'antecedentes': 'Antecedentes (RUT empresa, años de experiencia...)',
            'certificado_vigencia': 'Certificado de vigencia',
            'patente_comercial': 'Patente comercial',
            'poliza_seguro': 'Póliza de responsabilidad civil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in ['certificado_vigencia', 'patente_comercial', 'poliza_seguro']:
            self.fields[campo].required = True
            self.fields[campo].widget.attrs['accept'] = '.pdf'
