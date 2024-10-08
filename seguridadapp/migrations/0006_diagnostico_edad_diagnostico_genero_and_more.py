# Generated by Django 5.0.7 on 2024-08-07 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridadapp', '0005_rename_cardiopatia_diagnostico_cardiopatia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostico',
            name='Edad',
            field=models.FloatField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='Genero',
            field=models.FloatField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='Cardiopatia',
            field=models.FloatField(default=False),
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='EstadoFumador',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='Hipertension',
            field=models.FloatField(default=False),
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='TipoTrabajo',
            field=models.FloatField(max_length=200),
        ),
        migrations.AlterField(
            model_name='diagnostico',
            name='prediccion',
            field=models.FloatField(blank=True, default=False, null=True),
        ),
    ]
