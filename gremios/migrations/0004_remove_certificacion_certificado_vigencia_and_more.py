import django.db.models.deletion
import gremios.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gremios', '0003_certificacion_certificado_vigencia_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificacion',
            name='certificado_vigencia',
        ),
        migrations.RemoveField(
            model_name='certificacion',
            name='patente_comercial',
        ),
        migrations.RemoveField(
            model_name='certificacion',
            name='poliza_seguro',
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('archivo', models.FileField(upload_to='documentos', validators=[gremios.models.validar_pdf])),
                ('fecha', models.DateField(auto_now_add=True)),
                ('certificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='gremios.certificacion')),
            ],
        ),
    ]
