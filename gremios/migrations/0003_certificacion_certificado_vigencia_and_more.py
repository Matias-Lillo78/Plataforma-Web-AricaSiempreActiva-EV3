import gremios.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gremios', '0002_alter_certificacion_estado_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificacion',
            name='certificado_vigencia',
            field=models.FileField(blank=True, null=True, upload_to='documentos', validators=[gremios.models.validar_pdf]),
        ),
        migrations.AddField(
            model_name='certificacion',
            name='mensaje_admin',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='certificacion',
            name='patente_comercial',
            field=models.FileField(blank=True, null=True, upload_to='documentos', validators=[gremios.models.validar_pdf]),
        ),
        migrations.AddField(
            model_name='certificacion',
            name='poliza_seguro',
            field=models.FileField(blank=True, null=True, upload_to='documentos', validators=[gremios.models.validar_pdf]),
        ),
    ]
