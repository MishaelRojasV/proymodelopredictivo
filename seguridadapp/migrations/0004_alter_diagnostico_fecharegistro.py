# Generated by Django 5.0.7 on 2024-08-05 19:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridadapp', '0003_alter_diagnostico_fecharegistro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnostico',
            name='fechaRegistro',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
